# NLE utils

## Key features

## Installation

```bash
# NLE dependencies
apt-get install -yq autoconf libtool pkg-config libbz2-dev

conda create -n nle_utils python=3.10

python -m pip install --upgrade pip
pip install --upgrade setuptools

conda update -n base -c defaults conda
conda install -yq cmake flex bison lit

# install NLE
git clone https://github.com/BartekCupial/nle.git nle && cd nle \
&& git checkout fair_nle && git submodule init && git submodule update --recursive \
&& sed '/#define NLE_ALLOW_SEEDING 1/i#define NLE_ALLOW_SEEDING 1' include/nleobs.h -i \
&& sed '/self\.nethack\.set_initial_seeds = f/d' nle/env/tasks.py -i \
&& sed '/self\.nethack\.set_current_seeds = f/d' nle/env/tasks.py -i \
&& sed '/self\.nethack\.get_current_seeds = f/d' nle/env/tasks.py -i \
&& sed '/def seed(self, core=None, disp=None, reseed=True):/d' nle/env/tasks.py -i \
&& sed '/raise RuntimeError("NetHackChallenge doesn.t allow seed changes")/d' nle/env/tasks.py -i \
&& python setup.py install && cd .. 

# install render utils
pip install -e sf_examples/nethack/render_utils

# install NLE utils
pip install -e .[dev]

pre-commit install

# Test NLE.
python -c 'import gym; import nle; env = gym.make("NetHackScore-v0"); env.reset()'
```

## Quickstart

## Citation