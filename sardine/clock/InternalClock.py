from ..Components.BaseClock import BaseClock
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .FishBowl import FishBowl

class Clock(BaseClock):

    def __init__(self, env: 'FishBowl'):
        self._env = env

    def run(self):
        """Main loop for the internal clock"""
        while True:
            # Update clock state, and then:
            self._env.dispatch('tick')