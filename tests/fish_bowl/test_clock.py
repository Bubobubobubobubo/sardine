import asyncio
import math

import pytest
import rich
from rich.table import Table

from sardine import FishBowl, InternalClock

from . import EventLogHandler, Pauser, fish_bowl

PAUSE_DURATION = 0.1
ALWAYS_FAIL = False


@pytest.mark.asyncio
async def test_internal_clock(fish_bowl: FishBowl):
    EXPECTED_TOLERANCE = 0.024
    REAL_TOLERANCE = 0.00013
    # Calibrate above tolerances to acceptable levels

    assert isinstance(fish_bowl.clock, InternalClock)

    end_event = "test_internal_clock"
    event_order = ("start", "pause", "resume", "stop", end_event)

    logger = EventLogHandler(whitelist=event_order)
    fish_bowl.add_handler(logger)

    pauser = Pauser(logger.time, asyncio.sleep, origin=0.0)

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
    rows = zip(logger.events, pauser.real, pauser.expected)
    for event, real, expected in rows:
        clock = event.clock_time
        e_dev = clock - expected
        r_dev = clock - real
        table.add_row(str(clock), str(r_dev), str(e_dev))
    table.add_section()
    table.add_row("Tolerance", f"<{REAL_TOLERANCE}", f"<{EXPECTED_TOLERANCE}")
    rich.print(table)

    for event, rt, et in zip(logger.events, pauser.real, pauser.expected):
        assert math.isclose(event.clock_time, et, abs_tol=EXPECTED_TOLERANCE)
        assert math.isclose(event.clock_time, rt, abs_tol=REAL_TOLERANCE)

    assert not ALWAYS_FAIL, "ALWAYS_FAIL is enabled"
