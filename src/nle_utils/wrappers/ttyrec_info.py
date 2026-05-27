from pathlib import Path

import gymnasium as gym


class TtyrecInfoWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env, done_only=True):
        super().__init__(env)
        self.done_only = done_only

    def step(self, action):
        ttyrec = self.env.unwrapped.nethack._ttyrec
        obs, reward, term, trun, info = self.env.step(action)
        done = term or trun

        if done or self.done_only:
            extra_stats = info.get("episode_extra_stats", {})
            extra_stats["ttyrecname"] = Path(ttyrec).name if ttyrec else ""
            info["episode_extra_stats"] = extra_stats

        return obs, reward, term, trun, info
