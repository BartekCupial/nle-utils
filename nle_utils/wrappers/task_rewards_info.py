import copy

import gymnasium as gym

from nle_utils.task_rewards import (
    EatingScore,
    GoldScore,
    OracleScore,
    ScoutScore,
    SokobanFillPitScore,
    SokobanReachedScore,
    SokobanSolvedLevelsScore,
    SokobanSolvedScore,
    StaircasePetScore,
    StaircaseScore,
)


class TaskRewardsInfoWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env, done_only=True):
        super().__init__(env)
        self.done_only = done_only

        self.tasks = [
            EatingScore(),
            # GoldScore(),
            ScoutScore(),
            SokobanFillPitScore(),
            SokobanSolvedLevelsScore(),
            SokobanReachedScore(),
            SokobanSolvedScore(),
            StaircasePetScore(),
            StaircaseScore(),
            OracleScore(),
        ]

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)

        for task in self.tasks:
            task.reset_score()

        return obs, info

    def step(self, action):
        last_observation = copy.deepcopy(self.env.unwrapped.last_observation)
        obs, reward, term, trun, info = self.env.step(action)
        done = term or trun
        observation = copy.deepcopy(self.env.unwrapped.last_observation)
        end_status = info["end_status"]

        # we will accumulate rewards for each step and log them when done signal appears
        for task in self.tasks:
            task.reward(self.env.unwrapped, last_observation, observation, end_status)

        if done or not self.done_only:
            info["episode_extra_stats"] = self.episode_extra_stats(info, last_observation)

        return obs, reward, term, trun, info

    def episode_extra_stats(self, info, last_observation):
        extra_stats = info.get("episode_extra_stats", {})
        new_extra_stats = {task.name: task.score for task in self.tasks}
        return {**extra_stats, **new_extra_stats}
