import asyncio
import math
from typing import Callable

import pytest
from sardine import FishBowl, InternalClock

from . import EventLogHandler, fish_bowl

PAUSE_DURATION = 0.010
MAXIMUM_DEVIATION = 1e-9


class Pauser:
    def __init__(self, time_func: Callable[[], float], *, origin: float):
        self.time = time_func
        self.origin = origin
        self.stamps: list[float] = []

    async def sleep(self, duration: float, *, accumulate=True) -> float:
        start = self.time()
        await asyncio.sleep(duration)
        elapsed = self.time() - start

        if accumulate:
            elapsed += self.origin
            self.origin = elapsed

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
    for event, expected_time in zip(logger.events, pauser.stamps):
        assert math.isclose(
            event.clock_time, expected_time, abs_tol=MAXIMUM_DEVIATION
        )
