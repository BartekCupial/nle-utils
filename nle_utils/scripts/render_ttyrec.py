import argparse
from glob import glob
from pathlib import Path
from typing import Tuple

from nle_utils.parallel_utils import Result, run_parallel
from nle_utils.ttyrec.read_ttyrec import get_ttyrec_version
from nle_utils.ttyrec.render_ttyrec import RenderTtyrec
from nle_utils.utils import str2bool


def worker(name_path: Tuple[str, Path], output_dir: Path, ttyrec_version, show) -> Result:
    sample_name, ttyrec = name_path

    if get_ttyrec_version(ttyrec) is None:
        return Result(description=sample_name, log_msg="file is not ttyrec")

    renderer = RenderTtyrec(output_dir, ttyrec_version, show=show)
    renderer.render(ttyrec)
    renderer.close()

    return Result(description=sample_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ttyrec_dir", type=str)
    parser.add_argument("--output_dir", type=str)
    parser.add_argument("--ttyrec_version", type=int, default=3)
    parser.add_argument("--show", type=str2bool, default=False)
    parser.add_argument("--n_jobs", type=int, default=8)
    flags = parser.parse_args()
    print(flags)

    data = {Path(filename).name: filename for filename in glob(f"{flags.ttyrec_dir}/**/*ttyrec*", recursive=True)}
    total = len(data)
    run_parallel(
        function=worker,
        iterable=data.items(),
        function_args=(flags.output_dir, flags.ttyrec_version, flags.show),
        n_jobs=flags.n_jobs,
    )
