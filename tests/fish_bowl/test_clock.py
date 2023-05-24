import asyncio
import math
from typing import Type

import pytest
import rich
from rich.table import Table

from sardine_core import BaseClock, FishBowl, InternalClock, LinkClock

from . import EventLogHandler, Pauser, fish_bowl


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "clock_type,real_tol,expected_tol",
    [
        (InternalClock, 0.00025, 0.024),
        (LinkClock, 0.032, 0.034),
    ],
)
async def test_clock_sleeping(
    clock_type: Type[BaseClock],
    real_tol: float,
    expected_tol: float,
):
    PAUSE_DURATION = 0.1
    ALWAYS_FAIL = False

    fish_bowl = FishBowl(clock=clock_type())

    end_event = "test_finish"
    event_order = ("start", "pause", "resume", "stop", end_event)

    logger = EventLogHandler(whitelist=event_order)
    fish_bowl.add_handler(logger)

    pauser = Pauser(logger.time, asyncio.sleep)

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
    rows = zip(logger.events, pauser.cumulative_real, pauser.cumulative_expected)
    for event, real, expected in rows:
        clock = event.clock_time
        e_dev = clock - expected
        r_dev = clock - real
        table.add_row(str(clock), str(r_dev), str(e_dev))
    table.add_section()
    table.add_row("Tolerance", f"<{real_tol}", f"<{expected_tol}")
    rich.print(table)

    rows = zip(logger.events, pauser.cumulative_real, pauser.cumulative_expected)
    for event, rt, et in rows:
        assert math.isclose(event.clock_time, et, abs_tol=expected_tol)
        assert math.isclose(event.clock_time, rt, abs_tol=real_tol)

    assert not ALWAYS_FAIL, "ALWAYS_FAIL is enabled"
