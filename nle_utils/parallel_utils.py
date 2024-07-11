import multiprocessing as mp
from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Generic, Iterable, List, Optional, Sized, T, Union

import psutil
from tqdm.auto import tqdm

from nle_utils.collections import listify
from nle_utils.functional import apply, ifnone


def get_physical_cores_count() -> int:
    physical = psutil.cpu_count(logical=False)
    affinity = len(psutil.Process().cpu_affinity())
    return min(physical, affinity) if physical is not None else affinity


def per_call_parallel(calls: int, n_jobs: Optional[int] = None) -> int:
    # TODO: add docs and in future simplify usage
    cores = get_physical_cores_count()

    if n_jobs is None or n_jobs <= 0:
        n_jobs = cores

    n_jobs = min(n_jobs, max(calls, 1))

    return cores // n_jobs


@dataclass
class Result(Generic[T]):
    value: Optional[T] = None
    description: Optional[str] = ""
    log_msg: Optional[Union[str, List[str]]] = None


def imap_parallel(
    *,
    iterable: Iterable[Any],
    function: Callable[..., Result[T]],
    function_args: tuple,
    n_jobs: Optional[int] = None,
    ordered: bool = True,
) -> Iterable[T]:
    if n_jobs is None or n_jobs <= 0:
        n_jobs = get_physical_cores_count()

    tupled_function = partial(apply, function)
    args = ((item, *function_args) for item in iterable)
    total = len(iterable) if isinstance(iterable, Sized) else None

    if n_jobs > 1:
        pool = mp.Pool(processes=n_jobs)
        pool_map = pool.imap if ordered else pool.imap_unordered
        results = pool_map(tupled_function, args)
    else:
        results = map(tupled_function, args)

    with tqdm(results, total=total, leave=False) as progress:
        for result in progress:
            for log_msg in listify(ifnone(result.log_msg, [])):
                progress.write(result.description + ": " + log_msg)

            progress.set_description("done: " + result.description)

            yield result.value

    if n_jobs > 1:
        pool.close()


def map_parallel(
    *,
    iterable: Iterable[Any],
    function: Callable[..., Result[T]],
    function_args: tuple,
    n_jobs: Optional[int] = None,
) -> List[T]:
    values = imap_parallel(
        iterable=iterable,
        function=function,
        function_args=function_args,
        n_jobs=n_jobs,
    )

    return [*values]


def run_parallel(
    *,
    iterable: Iterable[Any],
    function: Callable[..., Result],
    function_args: tuple,
    n_jobs: Optional[int] = None,
    ordered: bool = False,
) -> None:
    values = imap_parallel(
        iterable=iterable,
        function=function,
        function_args=function_args,
        n_jobs=n_jobs,
        ordered=ordered,
    )

    for _ in values:
        # Force computation and discard results.
        pass
