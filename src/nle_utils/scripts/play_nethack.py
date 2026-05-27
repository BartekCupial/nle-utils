import contextlib
import os
import sys
import termios
import tty

from nle.nethack.actions import C, M

from nle_utils.cfg.arguments import parse_args, parse_full_cfg
from nle_utils.envs.env_utils import register_env
from nle_utils.envs.nethack.nethack_env import NETHACK_ENVS, make_nethack_env
from nle_utils.envs.nethack.nethack_params import add_extra_params_nethack_env
from nle_utils.play import play


@contextlib.contextmanager
def no_echo():
    tt = termios.tcgetattr(0)
    try:
        tty.setraw(0)
        yield
    finally:
        termios.tcsetattr(0, termios.TCSAFLUSH, tt)


def parse_numpad_action(action):
    """
    If the 'number_pad' option is on, keys usually used for movement can be
    used for various commands:

    n               followed by number of times to repeat the next command
    h     help      display one of several informative texts, like '?'
    j     jump      jump to another location
    k     kick      kick something (usually a door)
    l     loot      loot a box on the floor
    N     name      name an item or type of object
    u     untrap    untrap something (usually a trapped object)
    """

    numpad_actions = {
        # ord('n'): 'n',  # Repeat next command
        ord("h"): ord("?"),  # Help
        ord("j"): M("j"),  # Jump
        ord("k"): C("d"),  # Kick
        ord("l"): M("l"),  # Loot
        # ord('N'): 'N',  # Name
        ord("u"): M("u"),  # Untrap
        ord("1"): ord("b"),
        ord("2"): ord("j"),
        ord("3"): ord("n"),
        ord("4"): ord("h"),
        ord("5"): ord("."),
        ord("6"): ord("l"),
        ord("7"): ord("y"),
        ord("8"): ord("k"),
        ord("9"): ord("u"),
    }
    return numpad_actions.get(action, action)


def get_action(env, action_mode="human"):
    internal = env.unwrapped.last_observation[env.unwrapped._internal_index]
    in_yn_function = internal[1]
    in_getlin = internal[2]
    xwaitingforspace = internal[3]
    typing = in_yn_function or in_getlin or xwaitingforspace

    if action_mode == "random":
        action = env.action_space.sample()
    elif action_mode == "human":
        while True:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = os.read(fd, 3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

            if len(ch) == 1:
                if ord(ch) == 3:
                    raise KeyboardInterrupt
                elif ord(ch) < 32:
                    # ctrl was pressed
                    action = C(chr(ord(ch) + 64))
                else:
                    action = ord(ch)
                    if not typing:
                        action = parse_numpad_action(action)
            elif len(ch) == 2:
                if ch[0] == ord(b"\x1b"):
                    # alt was pressed
                    action = M(chr(ch[1]))
            elif len(ch) == 3:
                if ch == b"\x1b[A":
                    action = ord("k")
                elif ch == b"\x1b[B":
                    action = ord("j")
                elif ch == b"\x1b[C":
                    action = ord("l")
                elif ch == b"\x1b[D":
                    action = ord("h")
                # TODO add diagonals

            try:
                action = env.unwrapped.actions.index(action)
                break
            except ValueError:
                print(f"Selected action '{ch}' is not in action list. " "Please try again.")
                continue

    return action


def register_minihack_envs():
    for env_name in NETHACK_ENVS:
        register_env(env_name, make_nethack_env)


def register_minihack_components():
    register_minihack_envs()


def parse_minihack_args(argv=None):
    parser, partial_cfg = parse_args(argv=argv)
    add_extra_params_nethack_env(parser)
    final_cfg = parse_full_cfg(parser, argv)
    return final_cfg


def main():
    register_minihack_components()
    cfg = parse_minihack_args()
    play(cfg, get_action=get_action)


if __name__ == "__main__":
    main()
