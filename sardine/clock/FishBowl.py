from typing import TYPE_CHECKING
from ..sequences.LexerParser.ListParser import ListParser
from ..sequences.Iterators import Iterator
from ..sequences.Variables import Variables
from ..clock.InternalClock import Clock

if TYPE_CHECKING:
    from ..Components.BaseHandler import BaseHandler
    from .Time import Time
    from ..Components.BaseClock import BaseClock
    from ..Components.BaseParser import BaseParser

class FishBowl:
    def __init__(
        self,
        time: 'Time', 
    ):
        self._time = time
        self._clock = Clock(env=self, time=self._time, tempo=120, bpb=4)
        self._iterators = Iterator()
        self._variable = Variables() 
        self._handlers: list[BaseHandler] = []
        self._parser = ListParser(
            clock=self._clock,
            variables=self._variable,
            iterators=self._iterators
        )

    def add_clock(self, clock: 'BaseClock', **kwargs):
        """Hot-swap current clock for a different clock.

        Args:
            clock (BaseClock): Target clock
            **kwargs: argument for the new clock
        """
        self._clock = clock(env=self, time=self._time, **kwargs)
        
    def add_parser(self, parser: 'BaseParser'):
        """Hot-swap current parser for a different parser.

        Args:
            parser (BaseParser): New Parser
        """
        self._parser = parser(
            clock=self._clock,
            iterators=self._iterators,
            variables=self._variable
        )

    def add_handler(self, handler: 'BaseHandler'):
        """Adding a new handler to the environment. This handler will 
        receive all messages currently dispatched in the environment
        and react accordingly.

        Args:
            handler (BaseHandler): Sender
        """
        handler.setup(self)
        self._handlers.append(handler)

    def dispatch(self, event: str, *args, **kwargs):
        for handler in self._handlers:
            handler.hook(event, *args, **kwargs)

    @property
    def clock(self):
        return self._clock