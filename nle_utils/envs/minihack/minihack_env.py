from typing import Optional

import gymnasium as gym
import minihack  # NOQA: F401
from gymnasium import registry

from nle_utils.wrappers import AutoRender, AutoSeed

MINIHACK_ENVS = [env_spec.id for env_spec in registry.values() if "MiniHack" in env_spec.id]


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
        penalty_step=cfg.penalty_step,
        penalty_time=cfg.penalty_time,
        penalty_mode=cfg.fn_penalty_step,
        savedir=cfg.savedir,
        save_ttyrec_every=cfg.save_ttyrec_every,
    )

    if cfg.max_episode_steps is not None:
        kwargs["max_episode_steps"] = cfg.max_episode_steps

    if cfg.character is not None:
        kwargs["character"] = cfg.character

    if cfg.autopickup is not None:
        kwargs["autopickup"] = cfg.autopickup

    env = gym.make(env_name, render_mode=render_mode, **kwargs)
    env = AutoRender(env)
    env = AutoSeed(env)

    return env
