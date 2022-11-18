import time
from typing import (
    Any,
    Awaitable,
    Callable,
    Collection,
    Iterator,
    NamedTuple,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

import pytest_asyncio
from sardine import BaseHandler, FishBowl

__all__ = ("EventLogEntry", "EventLogHandler", "fish_bowl")

T = TypeVar("T")


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


def _get_last(seq: Sequence[T], default: T) -> T:
    return seq[-1] if seq else default


class Pauser:
    def __init__(
        self,
        time_func: Callable[[], float],
        sleep_func: Callable[[float], Awaitable[Any]],
        *,
        origin: float,
    ):
        self.time = time_func
        self._sleep = sleep_func
        self.origin = origin

        self.real: list[float] = []
        self.expected: list[float] = []

    async def sleep(self, duration: float, *, accumulate=True) -> float:
        start = self.time()
        await self._sleep(duration)
        elapsed = self.time() - start

        if accumulate:
            elapsed += self.origin
            self.origin = elapsed

        self.real.append(self.origin)

        last_stamp = _get_last(self.expected, self.origin)
        add_stamp = duration if accumulate else 0.0
        self.expected.append(last_stamp + add_stamp)


@pytest_asyncio.fixture
def fish_bowl() -> FishBowl:
    return FishBowl()
