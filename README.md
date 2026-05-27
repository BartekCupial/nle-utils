# nle-utils

Small Python utilities for working with the NetHack Learning Environment.

## Installation

Create and activate an environment:

```bash
conda create -n nle_utils python=3.10
conda activate nle_utils
```

Install NLE, then install this package from the local checkout:

```bash
MINOR=$(python -c 'import sys; print(f"cp{sys.version_info.major}{sys.version_info.minor}")')
pip install "https://github.com/BartekCupial/nle/releases/download/v1.2.1/nle-1.2.0-${MINOR}-${MINOR}-manylinux_2_17_$(uname -m).manylinux2014_$(uname -m).whl"

cd /home/bartek/Workspace/ideas/nle-utils
pip install -e ".[dev]"
pre-commit install
```

Check the install:

```bash
python -c 'import gymnasium as gym; import nle; env = gym.make("NetHackScore-v0"); env.reset()'
python -c 'import nle_utils; print("nle-utils ok")'
```
