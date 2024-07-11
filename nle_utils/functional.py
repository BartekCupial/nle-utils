from typing import Callable, TypeVar, Union

T = TypeVar("T")
U = TypeVar("U")


def identity(x: T) -> T:
    return x


def apply(func: Callable[..., T], args: tuple) -> T:
    return func(*args)


def ifnone(value: T, default: U) -> Union[T, U]:
    return value if value is not None else default
