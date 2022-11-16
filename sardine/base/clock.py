from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

__all__ = ("BaseClock",)


# TODO: document BaseClock and its methods
class BaseClock(ABC):
    env: 'FishBowl'

    @abstractmethod
    def run(self):
        """Starts the clock, updating the environment's clock state."""

    @property
    @abstractmethod
    def drift(self):
        pass

    @property
    @abstractmethod
    def time_grain(self):
        pass

    @property
    @abstractmethod
    def phase(self):
        pass

    @property
    @abstractmethod
    def beat(self):
        pass

    @property
    @abstractmethod
    def tempo(self):
        pass

    @property
    @abstractmethod
    def bpm(self):
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