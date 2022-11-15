from typing import TYPE_CHECKING
from ..sequences.LexerParser.ListParser import ListParser
from ..sequences.Iterators import Iterator
from ..sequences.Variables import Variables

if TYPE_CHECKING:
    from ..Components.BaseHandler import BaseHandler
    from .Time import Time
    from ..Components.BaseClock import BaseClock
    from ..Components.BaseParser import BaseParser

class FishBowl:
    def __init__(
        self,
        time: 'Time', 
        clock: 'BaseClock',
    ):
        self._time = time
        self._clock = clock
        self._iterators = Iterator()
        self._variable = Variables() 
        self._handlers: list[BaseHandler] = []
        self._parser = ListParser(
            clock=self._clock,
            variables=self._variable,
            iterators=self._iterators
        )
        
    def add_parser(self, parser: 'BaseParser'):
        self._parser = parser(
            clock=self._clock,
            iterators=self._iterators,
            variables=self._variable
        )

    def add_handler(self, handler: 'BaseHandler'):
        handler.setup(self)
        self._handlers.append(handler)

    def dispatch(self, event: str, *args, **kwargs):
        for handler in self._handlers:
            handler.hook(event, *args, **kwargs)