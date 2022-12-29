from dataclasses import dataclass
from typing import Any, Callable, Optional, ParamSpec, TypeVar

from ..base import BaseHandler
from ..handlers.sender import Number, NumericElement, Sender
from ..scheduler import AsyncRunner
from ..utils import alias_param, get_snap_deadline, lerp


@dataclass
class PatternInformation:
    sender: Sender
    send_method: Callable[P, T]
    args: tuple[Any]
    kwargs: dict[str, Any]
    period: NumericElement
    iterator: Optional[Number]
    divisor: NumericElement
    rate: NumericElement
    snap: Number
    timespan: Optional[float]


class ZifferPlayer(BaseHandler):

    """
    Experimental Ziffer Player
    """

    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self.runner = AsyncRunner(name=name)
        self.iterator: Number = 0
        self._iteration_span: Number = 1
        self._period: int | float = 1.0

    def __rshift__(self, pattern: Optional[PatternInformation]) -> None:
        ...

    def func(
        self,
        pattern: PatternInformation,
        p: NumericElement = 1,  # pylint: disable=invalid-name,unused-argument
    ) -> None:
        """Central swimming function defined by the player"""
        ...
        self.again(pattern=pattern, p=p)

    def push(self, pattern: Optional[PatternInformation]):
        """
        Managing lifetime of the pattern, similar to managing a swimming function
        manually. If PatternInformation is hot-swapped by None, the Player will stop
        scheduling its internal function, defined in self.func.
        """
        # This is a local equivalent to the silence() function.
        if pattern is None:
            return self.env.scheduler.stop_runner(self.runner)
        elif not self.runner.is_running():
            # Assume we are queuing the first state
            self.iterator = 0

        # Forcibly reset the interval shift back to 0 to make sure
        # the new pattern can be synchronized
        self.runner.interval_shift = 0.0

        period = self.get_new_period(pattern)

        deadline = get_snap_deadline(self.env.clock, pattern.snap)
        self.runner.push_deferred(deadline, self.func, pattern=pattern, p=period)

        self.env.scheduler.start_runner(self.runner)
        self.runner.reload()

    def again(self, *args, **kwargs):
        self.runner.update_state(*args, **kwargs)
        self.runner.swim()
