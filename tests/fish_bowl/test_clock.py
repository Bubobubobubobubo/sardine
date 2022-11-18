import asyncio
import math
from typing import Callable, Iterator

import pytest
import rich
from rich.table import Table

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

    @property
    def deviations(self) -> Iterator[float]:
        for rt, et in self.stamps_with_expected:
            yield rt - et

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

    table = Table("Step", "Clock", "Real", "Deviation")
    rows = zip(logger.events, pauser.stamps, pauser.deviations)
    for i, (event, real, dev) in enumerate(rows, start=1):
        clock = event.clock_time
        table.add_row(str(i), str(clock), str(real), str(dev))
    rich.print(table)

    for event, (rt, et) in zip(logger.events, pauser.stamps_with_expected):
        assert math.isclose(
            event.clock_time, rt, abs_tol=MAXIMUM_REAL_DEVIATION
        )
        assert math.isclose(rt, et, abs_tol=MAXIMUM_EXPECTED_DEVIATION)
