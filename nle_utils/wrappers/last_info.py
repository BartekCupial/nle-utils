import gym


class LastInfo(gym.Wrapper):
    def reset(self, **kwargs):
        obs = self.env.reset(**kwargs)
        self.last_info = None
        return obs

    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        self.last_info = info
        return obs, reward, done, info
