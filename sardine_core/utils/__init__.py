import functools
import inspect
from typing import TYPE_CHECKING, Callable, Literal, Optional, ParamSpec, TypeVar, Union

from .Messages import *

if TYPE_CHECKING:
    from ..base import BaseClock

P = ParamSpec("P")
T = TypeVar("T")

Number = Union[float, int]
Quant = Optional[Union[Number, Literal["now", "beat", "bar"]]]
Span = Optional[Union[Number, Literal['inf']]]

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


def get_deadline_from_quant(clock: "BaseClock", quant: Quant) -> Optional[float]:
    if quant == "now" or quant is None:
        return None
    elif quant == "beat":
        time = clock.shifted_time
        return time + clock.get_beat_time(1, time=time)
    elif quant == "bar":
        return get_deadline_from_quant(clock, 0)
    elif not isinstance(quant, (float, int)):
        raise ValueError(
            f"Invalid quant argument {quant!r}; must be 'now', 'beat', "
            f"'bar', None, or a numeric offset measured in beats"
        )

    time = clock.shifted_time
    next_bar = clock.get_bar_time(1, time=time)
    offset = clock.get_beat_time(quant, sync=False)
    return time + next_bar + offset


def lerp(
    x: Number,
    in_min: Number,
    in_max: Number,
    out_min: Number,
    out_max: Number,
) -> float:
    """Linearly interpolates a value v from range (x, y) to range (x', y')."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


async def maybe_coro(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


def plural(n: int, word: str, suffix: str = "s"):
    return word if n == 1 else word + suffix


def join(*args):
    """Alternative to the str.join function. Better in live contexts!

    Parameters:
    *args (list[string]): a list of strings to join with a whitespace

    Returns:
    list[string]: strings joined using ' '.join(args)

    """
    if all(isinstance(e, str) for e in args):
        return " ".join(args)
    else:
        return args[0]
