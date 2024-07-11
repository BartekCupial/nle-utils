from collections import namedtuple
from pathlib import Path

import cv2
from nle import nethack

from nle_utils.ttyrec.read_ttyrec import TTYREC_VERSION, ReadTtyrec
from nle_utils.visualize import Visualize

SmallerBLStats = namedtuple(
    "BLStats",
    "strength_percentage strength dexterity constitution intelligence wisdom charisma score hitpoints max_hitpoints depth gold energy max_energy armor_class monster_level experience_level experience_points time hunger_state carrying_capacity dungeon_number level_number prop_mask align",
)


class RenderTtyrec:
    def __init__(
        self,
        output_dir: str,
        ttyrec_version=TTYREC_VERSION,
        tileset_path="tilesets/3.6.1tiles32.png",
        tile_size=32,
        render_font_size=(18, 30),
        show: bool = False,
    ):
        self.output_dir = output_dir
        self.reader = ReadTtyrec(ttyrec_version)
        self.render_font_size = render_font_size
        self.show = show

        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # or use 'XVID' for .avi format
        self._window_name = "NetHack"

        self.visualizer = Visualize(tileset_path=tileset_path, tile_size=tile_size, render_font_size=render_font_size)

    def render(self, ttyrec: str):
        self.output_path = Path(self.output_dir) / f"{Path(ttyrec).stem}.mp4"
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.video_writer = cv2.VideoWriter(str(self.output_path), self.fourcc, 30.0, (1280, 720))

        stream = self.reader.read(ttyrec)

        for chars, colors, cursors, timestamps, actions, scores in stream:
            height = nethack.nethack.TERMINAL_SHAPE[0] * self.render_font_size[1]
            width = nethack.nethack.TERMINAL_SHAPE[1] * self.render_font_size[0]

            screen = self.visualizer._draw_tty(chars, colors, width, height)
            image = screen[..., ::-1]

            resized_image = cv2.resize(image, (1280, 720), cv2.INTER_AREA)
            self.video_writer.write(resized_image)

            if self.show:
                cv2.imshow(self._window_name, resized_image)
                cv2.waitKey(1)

        self.video_writer.release()

    def close(self):
        cv2.destroyAllWindows()
