from typing import TYPE_CHECKING
from .sequences.LexerParser.ListParser import ListParser
from .sequences.Iterators import Iterator
from .sequences.Variables import Variables
from .clock.InternalClock import Clock
from .clock.LinkClock import LinkClock

if TYPE_CHECKING:
    from .base.BaseHandler import BaseHandler
    from .clock.Time import Time
    from .base.BaseClock import BaseClock
    from .base.BaseParser import BaseParser


class FishBowl:
    def __init__(
        self,
        time: "Time",
    ):
        self.time = time
        # self.clock = Clock(env=self, tempo=120, bpb=4)
        self.clock = LinkClock(env=self, tempo=120, bpb=4)
        self.iterators = Iterator()
        self.variables = Variables()
        self.handlers: list[BaseHandler] = []
        self.parser = ListParser(env=self)

    def add_clock(self, clock: "BaseClock", **kwargs):
        """Hot-swap current clock for a different clock.

        Args:
            clock (BaseClock): Target clock
            **kwargs: argument for the new clock
        """
        self.clock = clock(env=self, **kwargs)

    def add_parser(self, parser: "BaseParser"):
        """Hot-swap current parser for a different parser.

        Args:
            parser (BaseParser): New Parser
        """
        self.parser = parser(env=self)

    def add_handler(self, handler: "BaseHandler"):
        """Adding a new handler to the environment. This handler will
        receive all messages currently dispatched in the environment
        and react accordingly.

        Args:
            handler (BaseHandler): Sender
        """
        handler.setup(self)
        self.handlers.append(handler)

    def dispatch(self, event: str, *args, **kwargs):
        for handler in self.handlers:
            handler.hook(event, *args, **kwargs)
