import bz2
import os
import re
import time
from typing import Literal

import numpy as np
from nle import nethack
from nle.dataset import Converter
from nle.nethack.actions import _ACTIONS_DICT

ROWS = 25
COLUMNS = 80
SEQ_LENGTH = 50

TTYREC_V1 = 1
TTYREC_V2 = 2
TTYREC_V3 = 3
TTYREC_VERSION = Literal[1, 2, 3]


def get_ttyrec_version(filename):
    pattern = r"ttyrec(\d*)"
    match = re.search(pattern, filename)

    if match:
        version = match.group(1)
        return int(version) if version else 1
    else:
        return None


class ReadTtyrec:
    def __init__(self, ttyrec_version: TTYREC_VERSION = TTYREC_V3):
        self.ttyrec_version = ttyrec_version
        self.converter = Converter(ROWS, COLUMNS, ttyrec_version)

        self.chars = np.zeros((SEQ_LENGTH, ROWS, COLUMNS), dtype=np.uint8)
        self.colors = np.zeros((SEQ_LENGTH, ROWS, COLUMNS), dtype=np.int8)
        self.cursors = np.zeros((SEQ_LENGTH, 2), dtype=np.int16)
        self.timestamps = np.zeros((SEQ_LENGTH,), dtype=np.int64)
        self.actions = np.zeros((SEQ_LENGTH), dtype=np.uint8)
        self.scores = np.zeros((SEQ_LENGTH), dtype=np.int32)

    def read(self, ttyrec: str):
        assert self.ttyrec_version == get_ttyrec_version(ttyrec)
        self.converter.load_ttyrec(ttyrec)

        while True:
            remaining = self.converter.convert(
                self.chars, self.colors, self.cursors, self.timestamps, self.actions, self.scores
            )
            end = np.shape(self.chars)[0] - remaining

            if end == 0:
                break

            for frame in range(end):
                yield (
                    self.chars[frame],
                    self.colors[frame],
                    self.cursors[frame],
                    self.timestamps[frame],
                    self.actions[frame],
                    self.scores[frame],
                )
