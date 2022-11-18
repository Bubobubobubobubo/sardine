import time
from typing import Any, Collection, Iterator, NamedTuple, Optional, Union

import pytest_asyncio
from sardine import BaseHandler, FishBowl

__all__ = ("EventLogEntry", "EventLogHandler", "fish_bowl")


class EventLogEntry(NamedTuple):
    """An event entry for the `EventLoggingHandler`."""

    timestamp: float
    clock_time: float
    event: str
    args: tuple[Any, ...]


class EventLogHandler(BaseHandler):
    """Logs events with timestamps, and optionally according to a whitelist."""

    def __init__(self, *, whitelist: Optional[Collection[str]] = None):
        super().__init__()
        self.whitelist = whitelist
        self.events: list[EventLogEntry] = []

    # Analysis methods

    def filter(
        self, events: Union[str, Collection[str]]
    ) -> Iterator[EventLogEntry]:
        if isinstance(events, str):
            events = (events,)

        for e in self.events:
            if e.event in events:
                yield e

    def time(self) -> float:
        return time.perf_counter()

    # Handler methods

    def setup(self):
        if self.whitelist is not None:
            for event in self.whitelist:
                self.register(event)
        else:
            self.register(None)

    def hook(self, event: str, *args):
        self.events.append(
            EventLogEntry(
                timestamp=self.time(),
                clock_time=self.env.clock.time,
                event=event,
                args=args,
            )
        )


@pytest_asyncio.fixture
def fish_bowl() -> FishBowl:
    return FishBowl()
