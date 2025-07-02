import gymnasium as gym


class LastInfo(gym.Wrapper):
    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self.last_info = None
        return obs, info

    def step(self, action):
        obs, reward, term, trun, info = self.env.step(action)
        self.last_info = info
        return obs, reward, term, trun, info
