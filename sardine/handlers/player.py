from ..base.handler import BaseHandler
from .midi import MidiHandler as MidiSender
from .superdirt import SuperDirtHandler as SuperDirtSender
from dataclasses import dataclass
from .osc import OSCHandler as OscSender
from ..scheduler import AsyncRunner
from typing import (
        Callable,
        Optional,
        Union,
        Tuple,
        Any
)

__all__ = ("Player",)

SENDER = Union[
        "MidiSender",
        "SuperDirtSender", 
        "OscSender"]

@dataclass
class PatternInformation:
    sender_method: Callable
    args: tuple
    kwargs: dict
    delay: Union[int, float]

class Player(BaseHandler):

    """
    Players are holders used to support one-line specialised swimming functions. Many 
    instances of 'Player' are injected in globals() at boot time as a way to provide a
    quick interface for the user to output musical and data patterns. Players are han-
    dling the whole lifetime of a pattern, from its initial entry in the scheduler to 
    its death when the silence() or panic() method is called.

    P1 >> d('bd', room=0.5, dry=0.2)
    P2 >> n(note='D@min7', velocity='80~100')
    """
    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self.runner: Optional['AsyncRunner'] = None
        self.pattern: Tuple[Tuple[Any], dict]
        self.delay: Union[int, float] = 1.0
        self.sender: SENDER
        self._events = {
        }

    @staticmethod
    def play(sender_method: Callable, *args, d, **kwargs): 
        """Entry point of a pattern into the Player"""
        return PatternInformation(sender_method, args, kwargs, d)

    def __rshift__(self, info: Optional[PatternInformation]) -> None:
        """
        This method acts as a cosmetic disguise for feeding PatternInformation into a 
        given player. Its syntax is inspired by FoxDot (Ryan Kirkbride), another very
        popular live coding library. 
        """
        self.push(pattern=info)

    def func(self, pattern: tuple, d: Union[int, float] = 1, i: int = 0) -> None:
        """Central swimming function defined by the player"""
        #TODO: implement me 
        self.sender(pattern)
        self.again(pattern, d=self.delay, i=i+1)

    def push(self, pattern: Optional[PatternInformation]):
        """
        Managing lifetime of the pattern, similar to managing a swimming function 
        manually. If PatternInformation is hot-swapped by None, the Player will stop
        scheduling its internal function, defined in self.func.
        """

        # This is a local equivalent to the silence() function.
        if pattern is None:
            return self.env.scheduler.stop_runner(self.runner)

        self.runner.push(self.func, pattern, d=self.delay)
        self.env.scheduler.start_runner(self.runner)

    def again(self, *args, **kwargs):
        self.runner.update_state(*args, **kwargs)
        self.runner.swim()

    def setup(self) -> None:
        for event in self._events:
            self.register(event)

    def hook(self, event: str, *args) -> None:
        func = self._events[event]
        func(*args)
