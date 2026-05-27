import gymnasium as gym


class AutoRender(gym.Wrapper):
    def reset(self, **kwargs):
        result = self.env.reset(**kwargs)
        if self.env.render_mode is not None:
            self.env.render()

        return result

    def step(self, action):
        result = self.env.step(action)
        if self.env.render_mode is not None:
            self.env.render()

        return result
