from ..base.handler import BaseHandler
from dataclasses import dataclass
from ..scheduler import AsyncRunner
from typing import (
        TYPE_CHECKING,
        TypeAlias,
        Optional,
)

if TYPE_CHECKING:
    from .midi import MidiHandler
    from .osc import OSCHandler
    from .superdirt import SuperDirtHandler

SENDER: TypeAlias = 'MidiHandler | OSCHandler | SuperDirtHandler'

__all__ = ("Player",)

@dataclass
class PatternInformation:
    sender: SENDER
    args: tuple
    kwargs: dict
    period: int | float | str
    iterator: int
    divisor: int
    rate: int | float

class Player(BaseHandler):

    """
    Players are holders used to support one-line specialised swimming functions. Many 
    instances of 'Player' are injected in globals() at boot time as a way to provide a
    quick interface for the user to output musical and data patterns. Players are han-
    dling the whole lifetime of a pattern, from its initial entry in the scheduler to 
    its death when the silence() or panic() method is called.
    """
    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self.runner = AsyncRunner(name=name)
        self._iteration_span: int = 1
        self._period: int | float = 1.0

    @property
    def iterator(self) -> int:
        """Internal iterator stored by the Player instance"""
        return self._iteration_span

    @iterator.setter
    def iterator(self, value: int) -> None:
        """Internal iterator stored by the Player instance"""
        self._iteration_span = value

    @staticmethod
    def play(
            sender: SENDER, 
            *args, 
            p: int | float | str, 
            i: int = 0,
            d: int = 1,
            r: int | float = 1.0,
            **kwargs): 
        """Entry point of a pattern into the Player"""
        return PatternInformation(
                sender=sender, 
                args=args,
                kwargs=kwargs,
                period=p,
                divisor=d,
                iterator=i,
                rate=r
        )

    def __rshift__(self, info: Optional[PatternInformation]) -> None:
        """
        This method acts as a cosmetic disguise for feeding PatternInformation into a 
        given player. Its syntax is inspired by FoxDot (Ryan Kirkbride), another very
        popular live coding library. 
        """
        self.push(pattern=info)

    def func(
            self, 
            pattern: PatternInformation, 
            p: int | float = 1,
            i: int= 0, 
            d: int = 1, 
            r: int | float = 1,
    ) -> None:
        """Central swimming function defined by the player"""

        pattern.sender.send(
                *pattern.args, 
                **pattern.kwargs,
                iterator=i, 
                divisor=d, 
                rate=r,
        )

        self.again(
                pattern=pattern, 
                p=pattern.period, 
                i=pattern.iterator+self._iteration_span,
                r=pattern.rate,
        )

    def push(self, pattern: Optional[PatternInformation]):
        """
        Managing lifetime of the pattern, similar to managing a swimming function 
        manually. If PatternInformation is hot-swapped by None, the Player will stop
        scheduling its internal function, defined in self.func.
        """

        # This is a local equivalent to the silence() function.
        if pattern is None:
            return self.env.scheduler.stop_runner(self.runner)

        self.runner.push(self.func, pattern=pattern, p=pattern.period)
        self.env.scheduler.start_runner(self.runner)
        self.runner.reload()

    def again(self, *args, **kwargs):
        self.runner.update_state(*args, **kwargs)
        self.runner.swim()
