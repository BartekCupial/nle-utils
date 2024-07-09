import re
import time
from pathlib import Path

import cv2
import gym
import numpy as np
import pandas as pd
from nle import nethack
from numba import njit
from PIL import Image, ImageDraw, ImageFont

from nle_utils.blstats import BLStats
from nle_utils.item import ItemClasses
from nle_utils.level import Level

HISTORY_SIZE = 13
FONT_SIZE = 32
RENDERS_HISTORY_SIZE = 128

SMALL_FONT_PATH = "Hack-Regular.ttf"

# Mapping of 0-15 colors used.
# Taken from bottom image here. It seems about right
# https://i.stack.imgur.com/UQVe5.png
COLORS = [
    "#000000",
    "#800000",
    "#008000",
    "#808000",
    "#000080",
    "#800080",
    "#008080",
    "#808080",  # - flipped these ones around
    "#C0C0C0",  # | the gray-out dull stuff
    "#FF0000",
    "#00FF00",
    "#FFFF00",
    "#0000FF",
    "#FF00FF",
    "#00FFFF",
    "#FFFFFF",
]


@njit
def _tile_characters_to_image(
    out_image,
    chars,
    colors,
    output_height_chars,
    output_width_chars,
    char_array,
    offset_h,
    offset_w,
):
    """
    Build an image using cached images of characters in char_array to out_image
    """
    char_height = char_array.shape[3]
    char_width = char_array.shape[4]
    for h in range(output_height_chars):
        h_char = h + offset_h
        # Stuff outside boundaries is not visible, so
        # just leave it black
        if h_char < 0 or h_char >= chars.shape[0]:
            continue
        for w in range(output_width_chars):
            w_char = w + offset_w
            if w_char < 0 or w_char >= chars.shape[1]:
                continue
            char = chars[h_char, w_char]
            color = colors[h_char, w_char]
            h_pixel = h * char_height
            w_pixel = w * char_width
            out_image[:, h_pixel : h_pixel + char_height, w_pixel : w_pixel + char_width] = char_array[char, color]


def _initialize_char_array(font_size, rescale_font_size):
    """Draw all characters in PIL and cache them in numpy arrays
    if rescale_font_size is given, assume it is (width, height)
    Returns a np array of (num_chars, num_colors, char_height, char_width, 3)
    """
    font = ImageFont.truetype(SMALL_FONT_PATH, font_size)
    dummy_text = "".join([(chr(i) if chr(i).isprintable() else " ") for i in range(256)])
    bboxes = np.array([font.getbbox(char) for char in dummy_text])
    image_width = bboxes[:, 2].max()
    image_height = bboxes[:, 3].max()

    char_width = rescale_font_size[0]
    char_height = rescale_font_size[1]
    char_array = np.zeros((256, 16, char_height, char_width, 3), dtype=np.uint8)

    for color_index in range(16):
        for char_index in range(256):
            char = dummy_text[char_index]

            image = Image.new("RGB", (image_width, image_height))
            image_draw = ImageDraw.Draw(image)
            image_draw.rectangle((0, 0, image_width, image_height), fill=(0, 0, 0))

            _, _, width, height = font.getbbox(char)
            x = (image_width - width) // 2
            y = (image_height - height) // 2
            image_draw.text((x, y), char, font=font, fill=COLORS[color_index])

            arr = np.array(image).copy()
            if rescale_font_size:
                arr = cv2.resize(arr, rescale_font_size, interpolation=cv2.INTER_AREA)
            char_array[char_index, color_index] = arr

    return char_array


def _draw_grid(imgs, ncol):
    grid = imgs.reshape((-1, ncol, *imgs[0].shape))
    rows = []
    for row in grid:
        rows.append(np.concatenate(row, axis=1))
    return np.concatenate(rows, axis=0)


def _put_text(img, text, pos, scale=FONT_SIZE / 32, thickness=1, color=(255, 255, 0), bg_color=None, bold=False):
    # TODO: figure out how exactly opencv anchors the text
    pos = (pos[0] + FONT_SIZE // 2, pos[1] + FONT_SIZE // 2 + 8)

    font = cv2.FONT_HERSHEY_PLAIN  # Monospaced font
    scale *= 2  # Adjust scale for better visibility in console

    if bg_color is not None:
        (text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)
        # Calculate the rectangle's position
        rect_pos = (pos[0], pos[1] - text_height - baseline)
        rect_end = (pos[0] + text_width, pos[1] + baseline)

        # Draw the background rectangle
        cv2.rectangle(img, rect_pos, rect_end, bg_color, -1)

    # Function to draw text
    def draw_text(offset_x=0, offset_y=0):
        text_pos = (int(pos[0] + offset_x), int(pos[1] + offset_y))
        cv2.putText(img, text, text_pos, font, scale, color, thickness, cv2.LINE_AA)

    if bold:
        # Draw the text multiple times with small offsets to create a bold effect
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                draw_text(offset_x, offset_y)
    else:
        # Draw the text once for normal weight
        draw_text()

    return img


def _put_tile(img, tile, pos):
    x, y, z = tile.shape
    img[pos[1] : pos[1] + y, pos[0] : pos[0] + x] = tile


def _draw_frame(img, color=(90, 90, 90), thickness=3):
    return cv2.rectangle(img, (0, 0), (img.shape[1] - 1, img.shape[0] - 1), color, thickness)


class RenderTiles(gym.Wrapper):
    def __init__(
        self,
        env: gym.Env,
        output_dir,
        tileset_path="tilesets/3.6.1tiles32.png",
        tile_size=32,
        render_font_size=(12, 22),
    ):
        super().__init__(env)

        self.output_dir = output_dir

        self.tileset = cv2.imread(tileset_path)[..., ::-1]
        if self.tileset is None:
            raise FileNotFoundError(f"Tileset {tileset_path} not found")
        if self.tileset.shape[0] % tile_size != 0 or self.tileset.shape[1] % tile_size != 0:
            raise ValueError("Tileset and tile_size doesn't match modulo")

        h = self.tileset.shape[0] // tile_size
        w = self.tileset.shape[1] // tile_size
        tiles = []
        for y in range(h):
            y *= tile_size
            for x in range(w):
                x *= tile_size
                tiles.append(self.tileset[y : y + tile_size, x : x + tile_size])
        self.tileset = np.array(tiles)
        from glyph2tile import glyph2tile

        self.glyph2tile = np.array(glyph2tile)

        self.video_writer = None
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # or use 'XVID' for .avi format

        self.action_history = list()
        self.message_history = list()
        self.popup_history = list()

        self._window_name = "NetHack"

        self.render_char_array = _initialize_char_array(FONT_SIZE, render_font_size)
        self.render_char_array = self.render_char_array.transpose(0, 1, 4, 2, 3)
        self.render_char_array = np.ascontiguousarray(self.render_char_array)

    def reset(self, **kwargs):
        self.start_time = time.time()

        if self.video_writer is not None:
            self.video_writer.release()

        obs = self.env.reset(**kwargs)

        self.output_path = Path(self.output_dir) / f"{Path(self.env.unwrapped.nethack._ttyrec).stem}.mp4"
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.video_writer = cv2.VideoWriter(str(self.output_path), self.fourcc, 30.0, (1920, 1080))

        self.render()
        return obs

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        self.render()

        self.action_history.append(self.env.unwrapped.actions[action].name)
        self.update_message_and_popup_history()

        return obs, reward, done, info

    def close(self):
        if self.video_writer is not None:
            self.video_writer.release()
            cv2.destroyAllWindows()
        return self.env.close()

    def render(self, **kwargs):
        glyphs = self.env.unwrapped.last_observation[self.env.unwrapped._glyph_index]

        tiles_idx = self.glyph2tile[glyphs]
        tiles = self.tileset[tiles_idx.reshape(-1)]
        scene_vis = _draw_grid(tiles, glyphs.shape[1])
        topbar = self._draw_topbar(scene_vis.shape[1])
        bottombar = self._draw_bottombar(scene_vis.shape[1])
        rendered = np.concatenate([topbar, scene_vis, bottombar], axis=0)

        inventory = self._draw_inventory(rendered.shape[0])
        rendered = np.concatenate([rendered, inventory], axis=1)

        image = rendered[..., ::-1]
        resized_image = cv2.resize(image, (1920, 1080), cv2.INTER_AREA)
        self.video_writer.write(resized_image)

        # if len(self.action_history) % 100 == 0:
        #     print(f"SPS: {(len(self.action_history) + 1) / (time.time() - self.start_time)}")

        # cv2.imshow(self._window_name, resized_image)
        # cv2.waitKey(1)

    def _draw_bottombar(self, width):
        obs = self.unwrapped.last_observation
        tty_chars = obs[self.unwrapped._observation_keys.index("tty_chars")]
        tty_colors = obs[self.unwrapped._observation_keys.index("tty_colors")]

        height = FONT_SIZE * len(tty_chars)
        tty = self._draw_tty(tty_chars, tty_colors, width - width // 2, height)
        stats = self._draw_stats(width // 2, height)
        return np.concatenate([tty, stats], axis=1)

    def _draw_tty(self, tty_chars, tty_colors, width, height):
        chw_image_shape = (
            3,
            nethack.nethack.TERMINAL_SHAPE[0] * self.render_char_array.shape[3],
            nethack.nethack.TERMINAL_SHAPE[1] * self.render_char_array.shape[4],
        )
        out_image = np.zeros(chw_image_shape, dtype=np.uint8)

        _tile_characters_to_image(
            out_image=out_image,
            chars=tty_chars,
            colors=tty_colors,
            output_height_chars=nethack.nethack.TERMINAL_SHAPE[0],
            output_width_chars=nethack.nethack.TERMINAL_SHAPE[1],
            char_array=self.render_char_array,
            offset_h=0,
            offset_w=0,
        )

        tty_image = out_image.transpose(1, 2, 0)
        tty = cv2.resize(tty_image, (width, height), interpolation=cv2.INTER_AREA)
        return tty

    def _draw_stats(self, width, height):
        ret = np.zeros((height, width, 3), dtype=np.uint8)
        blstats = BLStats(*self.env.unwrapped.last_observation[self.env.unwrapped._blstats_index])

        # game info
        i = 0
        txt = [
            f"Score:{blstats.score}",
            f"Step:{len(self.action_history)}",
            f"Turn:{blstats.time}",
            f"Dlvl:{blstats.level_number}",
            f"{' '.join(map(lambda x: x.capitalize(), Level(blstats.dungeon_number).name.split('_')))}",
        ]
        _put_text(ret, " ".join(txt), (0, i * FONT_SIZE), color=(255, 255, 255))
        i += 1

        # general character info
        txt = [
            f"St:{blstats.strength}",
            f"Dx:{blstats.dexterity}",
            f"Co:{blstats.constitution}",
            f"In:{blstats.intelligence}",
            f"Wi:{blstats.wisdom}",
            f"Ch:{blstats.charisma}",
        ]
        _put_text(ret, " ".join(txt), (0, i * FONT_SIZE))
        i += 1
        txt = [
            f"HP:{blstats.hitpoints}({blstats.max_hitpoints})",
            f"Pw:{blstats.energy}({blstats.max_energy})",
            f"AC:{blstats.armor_class}",
            f"Xp:{blstats.experience_level}/{blstats.experience_points}",
        ]
        _put_text(ret, " ".join(txt), (0, i * FONT_SIZE), color=(255, 255, 255))
        i += 2

        # extra stats info
        if self.last_info is not None:
            for k, v in self.last_info["episode_extra_stats"].items():
                txt = f"{' '.join(map(lambda x: x.capitalize(), k.split('_')))}: {v}"
                _put_text(ret, txt, (0, i * FONT_SIZE), color=(255, 255, 255))
                i += 1

        _draw_frame(ret)
        return ret

    def _draw_topbar(self, width):
        actions_vis = self._draw_action_history(np.round(width / 100 * 7).astype(int))
        messages_vis = self._draw_message_history(np.round(width / 100 * 43).astype(int))
        popup_vis = self._draw_popup_history(np.round(width / 100 * 50).astype(int))
        ret = np.concatenate([actions_vis, messages_vis, popup_vis], axis=1)
        assert ret.shape[1] == width
        return ret

    def _draw_action_history(self, width):
        vis = np.zeros((FONT_SIZE * HISTORY_SIZE, width, 3)).astype(np.uint8)
        for i in range(HISTORY_SIZE):
            if i >= len(self.action_history):
                break
            txt = self.action_history[-i - 1]
            if i == 0:
                _put_text(vis, txt, (0, i * FONT_SIZE), color=(255, 255, 255))
            else:
                _put_text(vis, txt, (0, i * FONT_SIZE), color=(120, 120, 120))
        _draw_frame(vis)
        return vis

    def _draw_message_history(self, width):
        messages_vis = np.zeros((FONT_SIZE * HISTORY_SIZE, width, 3)).astype(np.uint8)
        for i in range(HISTORY_SIZE):
            if i >= len(self.message_history):
                break
            txt = self.message_history[-i - 1]
            if i == 0:
                _put_text(messages_vis, txt, (0, i * FONT_SIZE), color=(255, 255, 255))
            else:
                _put_text(messages_vis, txt, (0, i * FONT_SIZE), color=(120, 120, 120))
        _draw_frame(messages_vis)
        return messages_vis

    def _draw_popup_history(self, width):
        messages_vis = np.zeros((FONT_SIZE * HISTORY_SIZE, width, 3)).astype(np.uint8)
        for i in range(HISTORY_SIZE):
            if i >= len(self.popup_history):
                break
            txt = "|".join(self.popup_history[-i - 1])
            if i == 0:
                _put_text(messages_vis, txt, (0, i * FONT_SIZE), color=(255, 255, 255))
            else:
                _put_text(messages_vis, txt, (0, i * FONT_SIZE), color=(120, 120, 120))
        _draw_frame(messages_vis)
        return messages_vis

    def update_message_and_popup_history(self):
        """Uses MORE action to get full popup and/or message."""
        message = self.env.unwrapped.last_observation[self.env.unwrapped._message_index]
        message = bytes(message).decode().replace("\0", " ").replace("\n", "").strip()
        if message.endswith("--More--"):
            # FIXME: It seems like in this case the environment doesn't expect additional input,
            #        but I'm not 100% sure, so it's too risky to change it, because it could stall everything.
            #        With the current implementation, in the worst case, we'll get "Unknown command ' '".
            message = message[: -len("--More--")]

        assert "\n" not in message and "\r" not in message
        popup = []

        tty_chars = self.env.unwrapped.last_observation[self.env.unwrapped._observation_keys.index("tty_chars")]
        lines = [bytes(line).decode().replace("\0", " ").replace("\n", "") for line in tty_chars]
        marker_pos, marker_type = self._find_marker(lines)

        if marker_pos is None:
            self.message_history.append(message)
            self.popup_history.append(popup)
            return

        pref = ""
        message_lines_count = 0
        if message:
            for i, line in enumerate(lines[: marker_pos[0] + 1]):
                if i == marker_pos[0]:
                    line = line[: marker_pos[1]]
                message_lines_count += 1
                pref += line.strip()

                # I'm not sure when the new line character in broken messages should be a space and when be ignored.
                # '#' character (and others) occasionally occurs at the beginning of the broken line and isn't in
                # the message. Sometimes the message on the screen lacks last '.'.
                def replace_func(x):
                    return "".join((c for c in x if c.isalnum()))

                if replace_func(pref) == replace_func(message):
                    break
            else:
                if marker_pos[0] == 0:
                    elems1 = [s for s in message.split() if s]
                    elems2 = [s for s in pref.split() if s]
                    assert len(elems1) < len(elems2) and elems2[-len(elems1) :] == elems1, (elems1, elems2)
                    return pref, popup, False
                raise ValueError(f"Message:\n{repr(message)}\ndoesn't match the screen:\n{repr(pref)}")

        # cut out popup
        for line in lines[message_lines_count : marker_pos[0]] + [lines[marker_pos[0]][: marker_pos[1]]]:
            line = line[marker_pos[1] :].strip()
            if line:
                popup.append(line)

        self.message_history.append(message)
        self.popup_history.append(popup)

    @staticmethod
    def _find_marker(lines, regex=re.compile(r"(--More--|\(end\)|\(\d+ of \d+\))")):
        """Return (line, column) of markers:
        --More-- | (end) | (X of N)
        """
        if len(regex.findall(" ".join(lines))) > 1:
            raise ValueError("Too many markers")

        result, marker_type = None, None
        for i, line in enumerate(lines):
            res = regex.findall(line)
            if res:
                assert len(res) == 1
                j = line.find(res[0])
                result, marker_type = (i, j), res[0]
                break

        if result is not None and result[1] == 1:
            result = (result[0], 0)  # e.g. for known items view
        return result, marker_type

    def _draw_inventory(self, height):
        width = 1000
        ret = np.zeros((height, width, 3), dtype=np.uint8)

        # get inventory
        obs = self.env.unwrapped.last_observation
        inv_glyphs = obs[self.env.unwrapped._observation_keys.index("inv_glyphs")]
        inv_letters = obs[self.env.unwrapped._observation_keys.index("inv_letters")]
        inv_oclasses = obs[self.env.unwrapped._observation_keys.index("inv_oclasses")]
        inv_strs = obs[self.env.unwrapped._observation_keys.index("inv_strs")]

        # don't show empty items
        number_of_items = len([i for i in inv_glyphs if i != 5976])
        inv_glyphs = inv_glyphs[:number_of_items]
        inv_letters = inv_letters[:number_of_items]
        inv_oclasses = inv_oclasses[:number_of_items]
        inv_strs = inv_strs[:number_of_items]

        inv_letters = list(map(chr, inv_letters))
        inv_oclasses = [ItemClasses(o).name for o in inv_oclasses]
        inv_strs = list(map(lambda x: "".join([chr(y) for y in x if y != 0]), inv_strs))

        items = dict(
            glyphs=inv_glyphs,
            letters=inv_letters,
            oclasses=inv_oclasses,
            strs=inv_strs,
        )
        items = pd.DataFrame(items)
        groups = {}
        for name, group in items.groupby("oclasses"):
            groups[name] = group

        i = 0
        for clas in ItemClasses:
            if clas.name in groups:
                txt = clas.name.capitalize()
                _put_text(ret, txt, (0, i * FONT_SIZE), color=(0, 0, 0), bg_color=(255, 255, 255), bold=True)
                i += 1

                for item in groups[clas.name].iloc:
                    txt = f"{item['letters']}) {item['strs']}"
                    glyph = item["glyphs"]
                    tiles_idx = self.glyph2tile[glyph]
                    tiles = self.tileset[tiles_idx]
                    _put_tile(ret, tiles, (16, i * FONT_SIZE))
                    _put_text(ret, txt, (40, i * FONT_SIZE), color=(255, 255, 255))
                    i += 1

                i += 1

        _draw_frame(ret)
        return ret
