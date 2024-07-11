import argparse
import ast
import sys
import time
import traceback
from multiprocessing import Pool
from pathlib import Path

import gym
import numpy as np
import pandas as pd

from nle_utils.ttyrec.render_ttyrec import RenderTtyrec
from nle_utils.utils import str2bool


def worker(flags):
    env = RenderTtyrec(flags.output_dir, flags.ttyrec_version, show=flags.show)
    env.render(flags.ttyrec)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ttyrec", type=str)
    parser.add_argument("--output_dir", type=str)
    parser.add_argument("--ttyrec_version", type=int, default=3)
    parser.add_argument("--show", type=str2bool, default=False)
    flags = parser.parse_args()
    print(flags)

    start_time = time.time()
    worker(flags)
