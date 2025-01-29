import gymnasium as gym


class SingleSeed(gym.Wrapper):
    def __init__(self, env, seed=None):
        super().__init__(env)
        self.seed = seed

    def reset(self, *, seed=None, options=None):
        return super().reset(seed=self.seed, options=options)
