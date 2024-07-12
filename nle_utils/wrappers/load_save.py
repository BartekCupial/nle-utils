import gym


class LoadSave(gym.Wrapper):
    def __init__(self, env: gym.Env, gameloaddir: str):
        super().__init__(env)
        self.gameloaddir = gameloaddir

    def reset(self, **kwargs):
        obs = self.env.reset(**kwargs)
        self.env.unwrapped.load(self.gameloaddir)
        return obs
