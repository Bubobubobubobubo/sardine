import time

import pytest

from sardine import FishBowl, InternalClock

from . import Pauser, fish_bowl


@pytest.mark.asyncio
async def test_sleep_internal_clock(fish_bowl: FishBowl):
    PAUSE_DURATION = 0.2
    ITERATIONS = 5
    TOLERANCE = 0.005 + 0.006 * ITERATIONS
    ALWAYS_FAIL = True

    assert isinstance(fish_bowl.clock, InternalClock)
    assert fish_bowl.clock.can_sleep()
    pauser = Pauser(time.perf_counter, fish_bowl.sleep, origin=0.0)

    fish_bowl.start()
    for _ in range(ITERATIONS):
        await pauser.sleep(PAUSE_DURATION)
    fish_bowl.stop()

    pauser.assert_equality(tolerance=TOLERANCE)

    assert not ALWAYS_FAIL, "ALWAYS_FAIL is enabled"
