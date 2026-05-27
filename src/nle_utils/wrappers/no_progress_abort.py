import gymnasium as gym
from nle import nethack


class NoProgressAbort(gym.Wrapper):
    def __init__(self, env, no_progress_timeout: int = 150):
        super().__init__(env)
        self.no_progress_timeout = no_progress_timeout
        # Monkey patch the internal abort check
        self.env.unwrapped._check_abort = self._check_abort
        self._last_checked_step = -1

    def reset(self, *args, **kwargs):
        self._turns = None
        self._no_progress_count = 0
        self._last_checked_step = -1
        return self.env.reset(*args, **kwargs)

    def _check_abort(self, observation):
        """Check if time has stopped and no observations has changed long enough
        to trigger an abort."""
        current_step = getattr(self.env.unwrapped, "_steps", 0)

        # Only update logic if we haven't processed this specific step yet
        if current_step != self._last_checked_step:
            turns = observation[self.env.unwrapped._blstats_index][nethack.NLE_BL_TIME]

            if self._turns == turns:
                self._no_progress_count += 1
            else:
                self._turns = turns
                self._no_progress_count = 0

            self._last_checked_step = current_step

        return (
            self.env.unwrapped._steps >= self.env.unwrapped._max_episode_steps
            or self._no_progress_count >= self.no_progress_timeout
        )
