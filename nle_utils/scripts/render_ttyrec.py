import argparse
import os
from glob import glob
from pathlib import Path
from typing import Tuple

from nle_utils.parallel_utils import Result, run_parallel
from nle_utils.ttyrec.read_ttyrec import get_ttyrec_version
from nle_utils.ttyrec.render_ttyrec import RenderTtyrec
from nle_utils.utils.utils import str2bool


def worker(ttyrec_path: str, output_dir: str, ttyrec_version, show) -> Result:
    sample_name = Path(ttyrec_path).name

    if get_ttyrec_version(ttyrec_path) is None:
        return Result(description=sample_name, log_msg="file is not ttyrec")

    renderer = RenderTtyrec(output_dir, ttyrec_version, show=show)
    renderer.render(ttyrec_path)
    renderer.close()

    return Result(description=sample_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ttyrec", type=str)
    parser.add_argument("--output_dir", type=str)
    parser.add_argument("--ttyrec_version", type=int, default=3)
    parser.add_argument("--show", type=str2bool, default=False)
    parser.add_argument("--n_jobs", type=int, default=8)
    flags = parser.parse_args()
    print(flags)

    if os.path.isdir(flags.ttyrec):
        data = [filename for filename in glob(f"{flags.ttyrec}/**/*ttyrec*", recursive=True)]
    else:
        data = (flags.ttyrec,)

    total = len(data)
    run_parallel(
        function=worker,
        iterable=data,
        function_args=(flags.output_dir, flags.ttyrec_version, flags.show),
        n_jobs=flags.n_jobs,
    )
