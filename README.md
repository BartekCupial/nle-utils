# NLE utils

## Key features

## Installation

```bash
conda create -n nle_utils python=3.10
MINOR=$(python3 -c 'import sys; print(f"cp{sys.version_info.major}{sys.version_info.minor}")')
pip install "https://github.com/BartekCupial/nle/releases/download/v1.2.1/nle-1.2.0-${MINOR}-${MINOR}-manylinux_2_17_$(uname -m).manylinux2014_$(uname -m).whl"

# install NLE utils
pip install -e .[dev]

pre-commit install

# Test NLE.
python -c 'import gymnasium as gym; import nle; env = gym.make("NetHackScore-v0"); env.reset()'
```

## Quickstart

## Citation