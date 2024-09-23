import contextlib
import os
import sys
import termios
import tty

from nle.nethack.actions import C, M

from nle_utils.envs.env_utils import register_env
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
    }
    return numpad_actions.get(action, action)


def get_action(env, action_mode, number_pad=True):
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
                    if number_pad:
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
                action = env.actions.index(action)
                break
            except ValueError:
                print(f"Selected action '{ch}' is not in action list. " "Please try again.")
                continue

    return action


def main():
    play()


if __name__ == "__main__":
    main()
