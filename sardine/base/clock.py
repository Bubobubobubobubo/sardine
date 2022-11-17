from abc import ABC, abstractmethod
import contextlib
import contextvars
from typing import TYPE_CHECKING, Optional

from .handler import BaseHandler

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

__all__ = ("BaseClock",)

time_shift = contextvars.ContextVar("time_shift", default=0.0)
"""
This specifies the amount of time to offset in the current context.
Usually this is updated within the context of scheduled functions
to simulate sleeping without actually blocking the function. Behavior is
undefined if time is shifted in the global context.
"""


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

        This number will also include any time shift that has been set.
        """
        time, origin = self.internal_time, self.internal_origin
        if time is None or origin is None:
            return self.env.time.origin
        return time - origin + self.env.time.origin + self.time_shift

    @property
    def time_shift(self) -> float:
        """The time shift in the current context.

        This is useful for simulating sleeps without blocking.
        """
        return time_shift.get()

    @time_shift.setter
    def time_shift(self, seconds: int):
        time_shift.set(seconds)

    @contextlib.contextmanager
    def scoped_time_shift(self, seconds: float):
        """Returns a context manager that adds `seconds` to the clock.

        After the context manager is exited, the time shift is restored
        to its previous value.
        """
        token = time_shift.set(time_shift.get() + seconds)
        try:
            yield
        finally:
            time_shift.reset(token)

    # Handler hooks

    def setup(self):
        pass  # TODO BaseClock setup()

    def teardown(self):
        pass  # TODO BaseClock teardown()

    def hook(self, event: str, *args):
        pass  # TODO BaseClock hook()
