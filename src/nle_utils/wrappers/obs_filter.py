from typing import List

import gymnasium as gym


class ObservationFilterWrapper(gym.ObservationWrapper):
    """
    A wrapper that filters the observation space to only include specified keys.

    Args:
        env: The environment to wrap
        keys: List of keys to keep in the observation space
    """

    def __init__(self, env: gym.Env, keys: List[str]):
        super().__init__(env)
        self.keys = keys

        # Verify all keys exist in original observation space
        if not isinstance(env.observation_space, gym.spaces.Dict):
            raise ValueError("ObservationFilterWrapper only works with Dict observation spaces")

        # Create new filtered observation space
        self.observation_space = gym.spaces.Dict(
            {key: env.observation_space.spaces[key] for key in keys if key in env.observation_space.spaces}
        )

    def observation(self, obs):
        """
        Filter the observation to only include specified keys.

        Args:
            obs: Original observation dictionary

        Returns:
            Filtered observation dictionary
        """
        return {key: obs[key] for key in self.observation_space.keys()}
