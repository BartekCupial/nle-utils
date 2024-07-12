from pathlib import Path

import cv2
import gym
from nle.nethack.actions import _ACTIONS_DICT

from nle_utils.visualize import Visualize


class RenderVideo(gym.Wrapper):
    def __init__(
        self,
        env: gym.Env,
        output_dir,
        tileset_path="tilesets/3.6.1tiles32.png",
        tile_size=32,
        render_font_size=(12, 22),
        show: bool = False,
    ):
        super().__init__(env)

        self.output_dir = output_dir
        self.show = show
        self.visualizer = Visualize(tileset_path=tileset_path, tile_size=tile_size, render_font_size=render_font_size)

        self.video_writer = None
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # or use 'XVID' for .avi format

        self._window_name = "NetHack"

    def reset(self, **kwargs):
        if self.video_writer is not None:
            self.video_writer.release()

        self.visualizer.reset_history()
        obs = self.env.reset(**kwargs)

        self.output_path = Path(self.output_dir) / f"{Path(self.env.unwrapped.nethack._ttyrec).stem}.mp4"
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.video_writer = cv2.VideoWriter(str(self.output_path), self.fourcc, 30.0, (1920, 1080))

        # TODO: add self.render() when updated to gymnasium
        return obs

    def step(self, action):
        obs, reward, done, info = self.env.step(action)

        # render current frame
        self.render()

        # add action, message and popup to history
        last_obs = self.env.unwrapped.last_observation
        message = last_obs[self.env.unwrapped._observation_keys.index("message")]
        tty_chars = last_obs[self.env.unwrapped._observation_keys.index("tty_chars")]
        self.visualizer.update_history(_ACTIONS_DICT[action], message, tty_chars)

        return obs, reward, done, info

    def render(self):
        last_obs = self.env.unwrapped.last_observation
        glyphs = last_obs[self.env.unwrapped._observation_keys.index("glyphs")]
        blstats = last_obs[self.env.unwrapped._observation_keys.index("blstats")]
        message = last_obs[self.env.unwrapped._observation_keys.index("message")]
        inv_glyphs = last_obs[self.env.unwrapped._observation_keys.index("inv_glyphs")]
        inv_letters = last_obs[self.env.unwrapped._observation_keys.index("inv_letters")]
        inv_oclasses = last_obs[self.env.unwrapped._observation_keys.index("inv_oclasses")]
        inv_strs = last_obs[self.env.unwrapped._observation_keys.index("inv_strs")]
        tty_chars = last_obs[self.env.unwrapped._observation_keys.index("tty_chars")]
        tty_colors = last_obs[self.env.unwrapped._observation_keys.index("tty_colors")]

        image = self.visualizer.render(
            glyphs,
            blstats,
            message,
            inv_glyphs,
            inv_letters,
            inv_oclasses,
            inv_strs,
            tty_chars,
            tty_colors,
        )

        resized_image = cv2.resize(image, (1920, 1080), cv2.INTER_AREA)
        self.video_writer.write(resized_image)

        if self.show:
            cv2.imshow(self._window_name, resized_image)
            cv2.waitKey(1)

    def close(self):
        if self.video_writer is not None:
            self.video_writer.release()
            cv2.destroyAllWindows()
        return self.env.close()
