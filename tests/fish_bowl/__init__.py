import time
from typing import Any, Collection, NamedTuple, Optional

import pytest_asyncio
from sardine import BaseHandler, FishBowl

__all__ = ("EventLog", "EventLoggingHandler", "fish_bowl")


class EventLog(NamedTuple):
    """An event entry for the `EventLoggingHandler`."""
    timestamp: float
    event: str
    args: tuple[Any, ...]


class EventLoggingHandler(BaseHandler):
    """Logs events with timestamps, and optionally according to a whitelist."""
    def __init__(self, whitelist: Optional[Collection[str]] = None):
        super().__init__()
        self.whitelist = whitelist
        self.events: list[EventLog] = []

    def setup(self):
        if self.whitelist is not None:
            for event in self.whitelist:
                self.register(event)
        else:
            self.register(None)

    def hook(self, event: str, *args):
        self.events.append(EventLog(time.monotonic(), event, args))


@pytest_asyncio.fixture
def fish_bowl() -> FishBowl:
    return FishBowl()
