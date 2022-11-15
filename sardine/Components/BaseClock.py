from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clock.Environment import Environment

class BaseClock(ABC):
    env: Environment

    @abstractmethod
    def run(self):
        """Starts the clock, updating the environment's clock state."""
        while True:
            # update the clock state, then:
            self.env.dispatch('tick')
