import asyncio
import math
from typing import Callable, Iterator

import pytest
import rich
from rich.table import Table

from sardine import FishBowl, InternalClock

from . import EventLogHandler, fish_bowl

PAUSE_DURATION = 0.1

EXPECTED_DEVIATION = 0.0125
# highly system-dependent, also exacerbated by PAUSE_DURATION

EXPECTED_TOLERANCE = 0.010
REAL_TOLERANCE = 0.0001
# Calibrate above tolerances to acceptable levels

ALWAYS_FAIL = False


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
                self.expected_stamps.append(
                    self.expected_stamps[-1]
                    + duration
                    + EXPECTED_DEVIATION
                )
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

    table = Table("Clock", "Performance Deviation", "Expected Deviation")
    rows = zip(logger.events, pauser.stamps_with_expected)
    for event, (real, expected) in rows:
        clock = event.clock_time
        e_dev = clock - expected
        r_dev = clock - real
        table.add_row(str(clock), str(r_dev), str(e_dev))
    table.add_section()
    table.add_row("Tolerance", f"<{REAL_TOLERANCE}", f"<{EXPECTED_TOLERANCE}")
    rich.print(table)

    for event, (rt, et) in zip(logger.events, pauser.stamps_with_expected):
        assert math.isclose(event.clock_time, et, abs_tol=EXPECTED_TOLERANCE)
        assert math.isclose(event.clock_time, rt, abs_tol=REAL_TOLERANCE)

    assert not ALWAYS_FAIL, 'ALWAYS_FAIL is enabled'
