import pickle
from pathlib import Path

import gym
import numpy as np


class NLEDemo(gym.Wrapper):
    """
    Records actions taken, creates checkpoints, allows time travel, restoring and saving of states
    """

    def __init__(self, env, gamesavedir):
        super().__init__(env)
        self.save_every_k = 100
        self.gamesavedir = gamesavedir
        self.savedir = Path(gamesavedir) / Path(self.env.unwrapped.nethack._ttyrec).stem

    def step(self, action):
        obs, reward, done, info = self.env.step(action)

        self.recorded_actions.append(action)
        self.rewards.append(reward)

        # periodic checkpoint saving
        if not done:
            if (
                len(self.checkpoint_action_nr) > 0
                and len(self.recorded_actions) >= self.checkpoint_action_nr[-1] + self.save_every_k
            ) or (len(self.checkpoint_action_nr) == 0 and len(self.recorded_actions) >= self.save_every_k):
                self.save_checkpoint()

        return obs, reward, done, info

    def reset(self):
        obs = self.env.reset()
        self.recorded_actions = []
        self.checkpoints = []
        self.checkpoint_action_nr = []
        self.rewards = []
        self.seeds = self.env.unwrapped.get_seeds()
        return obs

    def save_to_file(self):
        dat = {
            "actions": self.recorded_actions,
            "checkpoints": self.checkpoints,
            "checkpoint_action_nr": self.checkpoint_action_nr,
            "rewards": self.rewards,
            "seeds": self.seeds,
        }
        with open(self.savedir / "game.demo", "wb") as f:
            pickle.dump(dat, f)

    def load_from_file(self, file_name, demostep=-1):
        with open(file_name, "rb") as f:
            dat = pickle.load(f)
        self.recorded_actions = dat["actions"]
        self.checkpoints = dat["checkpoints"]
        self.checkpoint_action_nr = dat["checkpoint_action_nr"]
        self.rewards = dat["rewards"]
        self.seeds = dat["seeds"]
        self.env.unwrapped.seed(*self.seeds)
        obs = self.env.reset()

        if len(self.checkpoints) == 0:
            time_step = 0
        else:
            if 100 >= demostep >= 0:
                time_step = 0
            elif demostep >= 100:
                idx = np.where(np.array(self.checkpoint_action_nr) <= demostep)[0][-1]
                obs = self.env.unwrapped.load(self.checkpoints[idx])
                time_step = self.checkpoint_action_nr[idx]
            elif demostep == -1:
                idx = -1
                obs = self.env.unwrapped.load(self.checkpoints[idx])
                time_step = self.checkpoint_action_nr[idx]
            else:
                raise ValueError

        # IMPORTANT, to have reproducible trajectories we need to save checkpoints
        # e.g. if the trajectory was generated with saves every 100 actions
        # to reproduce it from saved action list we also need to save the game every 100 actions
        # this is because state of random generator changes when saving.
        # The issue would manifest itself e.g. with self.recorded_actions[time_step:] instead of self.recorded_actions[time_step:demostep]
        # TODO: maybe we can save the game differently idk. (We would have to create different C function for saving)
        for action in self.recorded_actions[time_step:demostep]:
            obs, _, done, _ = self.env.step(action)

            # TODO: we don't have any guarantees that dones won't happen, e.g. above issue
            # this would indicate issues with saving etc...
            assert not done, "issue with saving/loading happened..."

        return obs

    def save_checkpoint(self):
        i = len(self.recorded_actions)
        chk_pth = self.savedir / f"ckpt_{i}"
        self.env.unwrapped.save(gamesavedir=chk_pth)
        self.checkpoints.append(chk_pth)
        self.checkpoint_action_nr.append(len(self.recorded_actions))
