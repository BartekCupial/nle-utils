import setuptools
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()
    descr_lines = long_description.split("\n")
    descr_no_gifs = []  # gifs are not supported on PyPI web page
    for dl in descr_lines:
        if not ("<img src=" in dl and "gif" in dl):
            descr_no_gifs.append(dl)

    long_description = "\n".join(descr_no_gifs)


setup(
    # Information
    name="nle-utils",
    description="Utils for NLE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="2.1.2",
    url="https://github.com/BartekCupial/nle-utils",
    author="Bartłomiej Cupiał",
    license="MIT",
    keywords="nethack NLE utils ai",
    project_urls={
        "Github": "https://github.com/BartekCupial/nle-utils",
    },
    install_requires=[
        "opencv-python~=4.10",
        "numpy>=1.18.1,<2.0",
        "numba ~= 0.58",
        "pandas ~= 2.1",
        "matplotlib ~= 3.8",
        "seaborn ~= 0.12",
        "scipy ~= 1.11",
        "tqdm ~= 4.66",
        "debugpy ~= 1.6",
        "gymnasium",
    ],
    extras_require={
        # some tests require Atari and Mujoco so let's make sure dev environment has that
        "dev": ["black", "isort>=5.12", "pytest<8.0", "flake8", "pre-commit", "twine"]
    },
    package_dir={"": "./"},
    packages=setuptools.find_packages(where="./", include=["nle_utils*"]),
    include_package_data=True,
    python_requires=">=3.8",
)
