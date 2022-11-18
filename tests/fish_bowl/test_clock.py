import asyncio
import math
from typing import Callable, Iterator

import pytest

from sardine import FishBowl, InternalClock

from . import EventLogHandler, fish_bowl

PAUSE_DURATION = 0.050
MAXIMUM_REAL_DEVIATION = 1e-9
MAXIMUM_EXPECTED_DEVIATION = 1e-5


class Pauser:
    def __init__(self, time_func: Callable[[], float], *, origin: float):
        self.time = time_func
        self.origin = origin
        self.stamps: list[float] = []
        self.expected_stamps: list[float] = []

    @property
    def stamps_with_expected(self) -> Iterator[tuple[float, float]]:
        yield from zip(self.stamps, self.expected_stamps)

    async def sleep(self, duration: float, *, accumulate=True) -> float:
        start = self.time()
        await asyncio.sleep(duration)
        elapsed = self.time() - start

        if accumulate:
            elapsed += self.origin
            self.origin = elapsed

            if self.expected_stamps:
                self.expected_stamps.append(self.expected_stamps[-1] + duration)
        elif self.expected_stamps:
            self.expected_stamps.append(self.expected_stamps[-1])
        else:
            self.expected_stamps.append(self.origin)

        self.stamps.append(self.origin)


@pytest.mark.asyncio
async def test_internal_clock(fish_bowl: FishBowl):
    assert isinstance(fish_bowl.clock, InternalClock)

    end_event = "test_internal_clock"
    event_order = ("start", "pause", "resume", "stop", end_event)

    logger = EventLogHandler(whitelist=event_order)
    fish_bowl.add_handler(logger)

    pauser = Pauser(logger.time, origin=0.0)

    await pauser.sleep(PAUSE_DURATION, accumulate=False)
    fish_bowl.start()

    await pauser.sleep(PAUSE_DURATION)
    fish_bowl.pause()

    await pauser.sleep(PAUSE_DURATION, accumulate=False)
    fish_bowl.resume()

    await pauser.sleep(PAUSE_DURATION)
    fish_bowl.stop()

    await pauser.sleep(PAUSE_DURATION, accumulate=False)
    fish_bowl.dispatch(end_event)

    assert len(logger.events) == 5

    print("clock:", [e.clock_time for e in logger.events])
    print("slept:", pauser.stamps)
    print("expected:", pauser.expected_stamps)
    for event, (real_time, expected_time) in zip(logger.events, pauser.stamps_with_expected):
        assert math.isclose(
            event.clock_time, real_time, abs_tol=MAXIMUM_REAL_DEVIATION
        )
        assert math.isclose(
            real_time, expected_time, abs_tol=MAXIMUM_EXPECTED_DEVIATION
        )
