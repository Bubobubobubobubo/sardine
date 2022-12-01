import functools

from .Messages import *

MISSING = object()


def alias_param(name, alias):
    """
    Alias a keyword parameter in a function. Throws a TypeError when a value is
    given for both the original kwarg and the alias. Method taken from
    github.com/thegamecracks/abattlemetrics/blob/main/abattlemetrics/client.py
    (@thegamecracks).
    """

    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
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
