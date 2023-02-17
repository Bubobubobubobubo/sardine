from typing import Any, Callable, Optional, ParamSpec, TypeVar
from ..handlers.sender import Number, NumericElement, Sender
from ..utils import alias_param, get_snap_deadline, lerp
from ..scheduler import AsyncRunner
from dataclasses import dataclass
from ..base import BaseHandler

__all__ = ("ZifferPlayer",)

P = ParamSpec("P")
T = TypeVar("T")

@dataclass
class ZifferInformation:
    sender: Sender
    send_method: Callable[P, T]
    args: tuple[Any]
    kwargs: dict[str, Any]
    period: NumericElement
    timespan: Optional[float]




class ZifferPlayer(BaseHandler):

    """
    Specialised player dedicated to running a Ziffers pattern. Many instances of this 
    object  are injected in globals() at boot time as a way to provide a quick interface
    for the user to output musical and data patterns. Players are handling the whole 
    lifetime of a pattern, from its initial entry in the scheduler to its death when the
    silence() or panic() method is called.
    """

    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self.runner = AsyncRunner(name=name)
        self.iterator: Number = 0
        self._iteration_span: Number = 1
        self._period: int | float = 1.0

    @staticmethod
    @alias_param(name="period", alias="p")
    def play(
        sender: Sender,
        send_method: Callable[P, T],
        *args: P.args,
        timespan: Optional[float] = None,
        **kwargs: P.kwargs,
    ):
        """Entry point of a pattern into the Player"""

        return ZifferInformation(
            sender,
            send_method,
            args,
            kwargs,
            timespan,
        )

    def __rshift__(self, pattern: Optional[ZifferInformation]) -> None:
        """
        This method acts as a cosmetic disguise for feeding ZifferInformation into a
        given player. Its syntax is inspired by FoxDot (Ryan Kirkbride), another very
        popular live coding library. However, it is actually using Ziffers by Miika 
        Alonen :)
        """
        self.push(pattern)

    def func(
        self,
        pattern: ZifferInformation,
        p: NumericElement = 1,  # pylint: disable=invalid-name,unused-argument
    ) -> None:
        """Central swimming function defined by the player"""
        if pattern.iterator is not None:
            self.iterator = pattern.iterator
            pattern.iterator = None

        # Here, we are supposed to do something with the Ziffers Pattern.

        # pattern.send_method(
        #     *pattern.args,
        #     **pattern.kwargs,
        #     iterator=self.iterator,
        #     divisor=pattern.divisor,
        #     rate=pattern.rate,
        # )

        self.iterator += self._iteration_span
        period = 1 #FIX:Give me a Ziffers Period
        self.again(pattern=pattern, p=period)

    def push(self, pattern: Optional[ZifferInformation]):
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

        period = 1 #FIX: GIVE ME A ZIFFERS PERIOD

        deadline = get_snap_deadline(self.env.clock, pattern.snap)
        self.runner.push_deferred(deadline, self.func, pattern=pattern, p=period)

        self.env.scheduler.start_runner(self.runner)
        self.runner.reload()

    def again(self, *args, **kwargs):
        self.runner.update_state(*args, **kwargs)
        self.runner.swim()
