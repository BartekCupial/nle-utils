import re

import gymnasium as gym
from nle.nethack import actions as A


class AutoEscCallItem(gym.Wrapper):
    """
    A Wrapper for NLE that automatically skips calling an item.
    """

    def step(self, action):
        obs, reward, term, trun, info = self.env.step(action)

        # Note: we dont store the full message log here since the agent 
        # will never see the call prompt, so we dont need to aggregate it.
        while not (term or trun):
            msg = obs["text_message"]

            if re.match(r"^Call (a|an|the) .*:", msg):
                # Perform the auto-step: Press ESC to cancel the naming prompt
                obs, r, term, trun, info = self.env.step(self.env.actions.index(A.Command.ESC))
                reward += r

                if term or trun:
                    break

            else:
                # No prompt detected, return control to agent
                break

        return obs, reward, term, trun, info
