from typing import Optional

import gym
import nle  # NOQA: F401
from nle import nethack

from nle_utils.wrappers import GymV21CompatibilityV0, NLETimeLimit

NETHACK_ENVS = []
for env_spec in gym.envs.registry.all():
    id = env_spec.id
    if "NetHack" in id:
        NETHACK_ENVS.append(id)


def make_nethack_env(env_name, cfg, env_config, render_mode: Optional[str] = None):
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
        wizard=False,
        allow_all_yn_questions=True,
        allow_all_modes=True,
        actions=nethack.ACTIONS,
    )

    if cfg.max_episode_steps is not None:
        kwargs["max_episode_steps"] = cfg.max_episode_steps

    if cfg.autopickup is not None:
        kwargs["autopickup"] = cfg.autopickup

    env = gym.make(env_name, **kwargs)

    # wrap NLE with timeout
    env = NLETimeLimit(env)

    env = GymV21CompatibilityV0(env=env, render_mode=render_mode)

    return env
