import time

from nle import nethack
from nle.nethack.actions import _ACTIONS_DICT

from nle_utils.ttyrec.read_ttyrec import TTYREC_VERSION, ReadTtyrec


class PrintTtyrec:
    def __init__(self, ttyrec_version=TTYREC_VERSION):
        self.reader = ReadTtyrec(ttyrec_version)

    def render(self, ttyrec: str):
        stream = self.reader.read(ttyrec)

        start = time.time()
        i = 0
        for chars, colors, cursors, timestamps, actions, scores in stream:
            elapsed = time.time() - start
            print(nethack.tty_render(chars, colors, cursors))
            print(f"SPS: {i / elapsed}")
            print(f"Timestamp: {timestamps}")
            print(f"action: {_ACTIONS_DICT[actions]}")
            i += 1

        print("finished")
