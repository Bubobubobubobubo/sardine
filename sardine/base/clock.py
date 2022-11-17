from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from .handler import BaseHandler

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

__all__ = ("BaseClock",)


# TODO: document BaseClock and its methods
class BaseClock(BaseHandler, ABC):
    """The base for all clocks to inherit from.

    This interface expects clocks to manage its own source of time,
    and provide the `phase`, `beat`, and `tempo` properties.
    """

    env: "FishBowl"

    # Abstract methods

    @property
    @abstractmethod
    def internal_time(self) -> Optional[float]:
        """Returns the clock's internal time if available.

        At the start of the `run()` method, this should be set as early
        as possible in order for the `time` property to compute the
        elapsed time.
        """

    @property
    @abstractmethod
    def internal_origin(self) -> Optional[float]:
        """Returns the clock's internal time origin if available.

        At the start of the `run()` method, this should be set as early
        as possible in order for the `time` property to compute the
        elapsed time.
        """

    @abstractmethod
    def run(self):
        """Starts the clock, updating the environment's clock state."""

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

    # Properties

    @property
    def time(self) -> float:
        """Returns the current time of the fish bowl.

        This uses the `internal_time` and `internal_origin` properties
        along with the fish bowl's `Time.origin` to calculate a monotonic
        time for the entire system.

        This number will also add any `Time.shift` that has been applied.
        """
        time, origin = self.internal_time, self.internal_origin
        if time is None or origin is None:
            return self.env.time.origin
        return time - origin + self.env.time.origin + self.env.time.shift

    # Handler hooks

    def setup(self):
        pass  # TODO BaseClock setup()

    def teardown(self):
        pass  # TODO BaseClock teardown()

    def hook(self, event: str, *args):
        pass  # TODO BaseClock hook()
