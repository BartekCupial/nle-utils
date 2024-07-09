from pathlib import Path

import gym


class TtyrecInfoWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env, done_only=True):
        super().__init__(env)
        self.done_only = done_only

    def step(self, action):
        ttyrec = self.env.unwrapped.nethack._ttyrec
        obs, reward, done, info = self.env.step(action)

        if done or self.done_only:
            extra_stats = info.get("episode_extra_stats", {})
            extra_stats["ttyrecname"] = Path(ttyrec).name
            info["episode_extra_stats"] = extra_stats

        return obs, reward, done, info
