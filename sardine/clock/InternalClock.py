from ..Components.BaseClock import BaseClock
from typing import TYPE_CHECKING
import asyncio

if TYPE_CHECKING:
    from .FishBowl import FishBowl
    from .Time import Time

class Clock(BaseClock):

    def __init__(self, env: 'FishBowl', time: 'Time'):
        self._env = env
        self._time = time
        self._time_grain = 0.01

    def start(self):
        asyncio.create_task(self.run())

    async def run(self):
        """Main loop for the internal clock"""
        while True:
            # Update clock state, and then:
            self._time._phase += self._time_grain
            await asyncio.sleep(0.0)
            self._env.dispatch('tick')