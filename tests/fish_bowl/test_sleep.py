import time

import pytest

from sardine import FishBowl, InternalClock, MissileMode

from . import Pauser, fish_bowl


@pytest.mark.asyncio
async def test_sleep_internal_clock(fish_bowl: FishBowl):
    PAUSE_DURATION = 0.02
    ITERATIONS = 10
    TOLERANCE = 0.016
    ALWAYS_FAIL = False

    assert isinstance(fish_bowl.clock, InternalClock)
    assert fish_bowl.clock.can_sleep()

    # fish_bowl.add_handler(MissileMode(burn_rate=71.428))

    pauser = Pauser(time.perf_counter, fish_bowl.sleep)

    fish_bowl.start()
    for _ in range(ITERATIONS):
        await pauser.sleep(PAUSE_DURATION)
    fish_bowl.stop()

    pauser.assert_equality(tolerance=TOLERANCE)

    assert not ALWAYS_FAIL, "ALWAYS_FAIL is enabled"
