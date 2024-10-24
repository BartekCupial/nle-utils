from typing import Callable, List, Optional

import minihack  # NOQA: F401
import gym

from nle_utils.utils.utils import is_module_available
from nle_utils.wrappers import GymV21CompatibilityV0, NLETimeLimit


def minihack_available():
    return is_module_available("minihack")


MINIHACK_ENVS = []
for env_spec in gym.envs.registry.all():
    id = env_spec.id
    if id.split("-")[0] == "MiniHack":
        MINIHACK_ENVS.append(id)


def make_minihack_env(env_name, cfg, env_config, render_mode: Optional[str] = None):
    observation_keys = (
        "message",
        "blstats",
        "tty_chars",
        "tty_colors",
        "tty_cursor",
        # ALSO AVAILABLE (OFF for speed)
        # "specials",
        # "colors",
        # "chars",
        "glyphs",
        "inv_glyphs",
        "inv_strs",
        "inv_letters",
        "inv_oclasses",
    )

    kwargs = dict(
        observation_keys=observation_keys,
        character=cfg.character,
        penalty_step=cfg.penalty_step,
        penalty_time=cfg.penalty_time,
        penalty_mode=cfg.fn_penalty_step,
        savedir=cfg.savedir,
        save_ttyrec_every=cfg.save_ttyrec_every,
        autopickup=cfg.autopickup,
    )

    if cfg.max_episode_steps is not None:
        kwargs["max_episode_steps"] = cfg.max_episode_steps

    env = gym.make(env_name, **kwargs)

    # wrap NLE with timeout
    env = NLETimeLimit(env)

    env = GymV21CompatibilityV0(env=env)

    if render_mode:
        env.render_mode = render_mode

    return env
