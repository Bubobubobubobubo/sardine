from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .BaseHandler import BaseHandler

class Environment:
    clock_state: ClockState
    clock: BaseClock
    handlers: list[BaseHandler]
    parser: BaseParser

    def add_handler(self, handler: BaseHandler):
        handler.setup(self)
        self.handlers.append(handler)

    def dispatch(self, event: str, *args, **kwargs):
        for handler in self.handlers:
            handler.hook(event, *args, **kwargs)
