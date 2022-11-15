from typing import TYPE_CHECKING

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
        parser: 'BaseParser'
    ):
        self._time = time
        self._clock = clock
        self._parser = parser
        self._handlers: list[BaseHandler] = []

    def add_handler(self, handler: 'BaseHandler'):
        handler.setup(self)
        self.handlers.append(handler)

    def dispatch(self, event: str, *args, **kwargs):
        for handler in self.handlers:
            handler.hook(event, *args, **kwargs)