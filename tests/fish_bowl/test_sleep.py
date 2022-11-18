import asyncio
import math
import time

import pytest
import rich
from rich.table import Table

from sardine import FishBowl, InternalClock

from . import Pauser, fish_bowl

PAUSE_DURATION = 0.1
ALWAYS_FAIL = True


@pytest.mark.asyncio
async def test_internal_clock(fish_bowl: FishBowl):
    TOLERANCE = 0.001

    assert isinstance(fish_bowl.clock, InternalClock)
    pauser = Pauser(time.perf_counter, fish_bowl.sleep, origin=0.0)

    fish_bowl.start()
    for _ in range(5):
        await pauser.sleep(PAUSE_DURATION)
    fish_bowl.stop()

    for real, expected in zip(pauser.real, pauser.expected):
        assert math.isclose(real, expected, abs_tol=TOLERANCE)

    assert not ALWAYS_FAIL, "ALWAYS_FAIL is enabled"
