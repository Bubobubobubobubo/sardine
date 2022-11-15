from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .BaseHandler import BaseHandler
    from .Time import Time
    from .BaseClock import BaseClock

class Environment:
    clock_state: Time
    clock: BaseClock
    handlers: list[BaseHandler]
    parser: BaseParser

    def add_handler(self, handler: BaseHandler):
        handler.setup(self)
        self.handlers.append(handler)

    def dispatch(self, event: str, *args, **kwargs):
        for handler in self.handlers:
            handler.hook(event, *args, **kwargs)
