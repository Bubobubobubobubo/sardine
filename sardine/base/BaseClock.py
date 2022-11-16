from abc import ABC, abstractmethod, abstractproperty
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..FishBowl import FishBowl

class BaseClock(ABC):
    env: 'FishBowl'

    @abstractmethod
    def run(self):
        """Starts the clock, updating the environment's clock state."""
        while True:
            # update the clock state, then:
            self.env.dispatch('tick')

    @abstractproperty
    def drift():
        pass

    @abstractproperty
    def time_grain():
        pass

    @abstractproperty
    def phase():
        pass

    @abstractproperty
    def beat():
        pass

    @abstractproperty
    def tempo():
        pass

    @abstractproperty
    def bpm():
        pass

    @abstractmethod
    def pause(self):
        pass
    
    @abstractmethod
    def resume(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def is_running(self):
        pass

    @abstractmethod
    def is_paused(self):
        pass