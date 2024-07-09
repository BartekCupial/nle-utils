import gym
from nle import nethack

from nle_utils.blstats import BLStats


class FinalStatsWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env, done_only=False):
        super().__init__(env)
        self.done_only = done_only

    def reset(self, **kwargs):
        self.step_num = 0
        self.max_dlvl = 1
        self.current_dlvl = 1
        self.previous_dlvl = (0, 0)
        self.reached_levels = dict()
        self.reached_levels[(0, 0)] = dict(
            previous_level=self.previous_dlvl,
            dlvl=0,
        )

        return self.env.reset(**kwargs)

    def step(self, action):
        # use tuple and copy to avoid shallow copy (`last_observation` would be the same as `observation`)
        last_observation = tuple(a.copy() for a in self.env.unwrapped.last_observation)
        obs, reward, done, info = self.env.step(action)
        self.step_num += 1

        if done or not self.done_only:
            info["episode_extra_stats"] = self.episode_extra_stats(info, last_observation)

        return obs, reward, done, info

    def episode_extra_stats(self, info, observation):
        extra_stats = info.get("episode_extra_stats", {})

        blstats = BLStats(*observation[self.env.unwrapped._blstats_index])

        dungeon_num = blstats[nethack.NLE_BL_DNUM]
        dungeon_level = blstats[nethack.NLE_BL_DLEVEL]
        key = (dungeon_num.item(), dungeon_level.item())

        if key not in self.reached_levels:
            self.reached_levels[key] = dict(
                previous_level=self.previous_dlvl, dlvl=self.reached_levels[self.previous_dlvl]["dlvl"] + 1
            )
        self.previous_dlvl = key
        self.current_dlvl = self.reached_levels[key]["dlvl"]
        self.max_dlvl = max(self.max_dlvl, self.current_dlvl)

        blstats = blstats._asdict()
        include = [
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
            "hitpoints",
            "max_hitpoints",
            "gold",
            "energy",
            "max_energy",
            "armor_class",
            "experience_level",
            "experience_points",
            "score",
        ]
        blstats_info = dict(filter(lambda item: item[0] in include, blstats.items()))

        return {
            **extra_stats,
            **blstats_info,
            "step": self.step_num,
            "max_dlvl": self.max_dlvl,
            "dlvl": self.current_dlvl,
        }
