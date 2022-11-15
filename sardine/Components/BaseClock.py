from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clock.FishBowl import FishBowl

class BaseClock(ABC):
    env: 'FishBowl'

    @abstractmethod
    def run(self):
        """Starts the clock, updating the environment's clock state."""
        while True:
            # update the clock state, then:
            self.env.dispatch('tick')

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def stop(self):
        pass
