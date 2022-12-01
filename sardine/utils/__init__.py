import functools
from typing import Callable, ParamSpec, TypeVar

from .Messages import *

P = ParamSpec("P")
T = TypeVar("T")

MISSING = object()


def alias_param(name: str, alias: str):
    """
    Alias a keyword parameter in a function. Throws a TypeError when a value is
    given for both the original kwarg and the alias. Method taken from
    github.com/thegamecracks/abattlemetrics/blob/main/abattlemetrics/client.py
    (@thegamecracks).
    """

    def deco(func: Callable[P, T]):
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            alias_value = kwargs.pop(alias, MISSING)
            if alias_value is not MISSING:
                if name in kwargs:
                    raise TypeError(f"Cannot pass both {name!r} and {alias!r} in call")
                kwargs[name] = alias_value
            return func(*args, **kwargs)

        return wrapper

    return deco


def plural(n: int, word: str, suffix: str = "s"):
    return word if n == 1 else word + suffix
