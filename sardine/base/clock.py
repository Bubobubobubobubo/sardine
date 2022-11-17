from abc import ABC, abstractmethod
import asyncio
from typing import TYPE_CHECKING, Optional

from .handler import BaseHandler

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

__all__ = ("BaseClock",)


class BaseClock(BaseHandler, ABC):
    """The base for all clocks to inherit from.

    This interface expects clocks to manage its own source of time
    and provide the `phase`, `beat`, and `tempo` properties.

    Attributes:
        internal_origin:
            The clock's internal time origin if available, measured in seconds.
            At the start of the `run()` method, this should be set as early
            as possible in order for the `time` property to compute the
            elapsed time.
        internal_time:
            The clock's internal time if available, measured in seconds.
            This attribute should be continuously updated when the
            clock starts so the `time` property is able to move forward.
    """

    def __init__(self):
        super().__init__()
        self._run_task: Optional[asyncio.Task] = None
        self.internal_origin: Optional[float] = None
        self.internal_time: Optional[float] = None

    def __repr__(self) -> str:
        return (
            "({name} {0.time:1f}) -> [{0.tempo}|{0.bar:1f}: "
            "{0.phase}/{0.beats_per_bar}]"
        ).format(self, name=type(self).__name__)

    # Abstract methods

    @abstractmethod
    async def run(self):
        """The main run loop of the clock.

        This should setup any external time source, assign the current
        time to `internal_origin`, and then continuously
        update the `internal_time`.
        """

    @property
    @abstractmethod
    def bar(self) -> int:
        """The bar of the clock's current time."""

    @property
    @abstractmethod
    def beat(self) -> int:
        """The beat of the clock's current time."""

    @property
    @abstractmethod
    def beats_per_bar(self) -> int:
        """The number of beats in each bar."""

    @property
    @abstractmethod
    def phase(self) -> int:
        """The phase of the clock's current beat."""

    @property
    @abstractmethod
    def tempo(self) -> int:
        """The clock's current tempo."""

    # Properties

    @property
    def time(self) -> float:
        """Returns the current time of the fish bowl.

        This uses the `internal_time` and `internal_origin` attributes
        along with the fish bowl's `Time.origin` to calculate a monotonic
        time for the entire system.

        This number will also add any `Time.shift` that has been applied.

        If the fish bowl has been paused or stopped, `Time.origin` will be set
        to the latest value provided by `internal_time`, and this property
        will return `Time.origin` until the fish bowl resumes or starts again.

        If either the `internal_time` or `internal_origin` attributes
        are not available (i.e. they are set to `None`), this will default
        to the `Time.origin`. This should ideally be minimized so the clock
        can run as soon as possible.
        """
        if self.env.is_paused() or not self.env.is_running():
            return self.env.time.origin

        i_time, i_origin = self.internal_time, self.internal_origin
        if i_time is None or i_origin is None:
            return self.env.time.origin

        return i_time - i_origin + self.env.time.origin + self.env.time.shift

    def is_running(self) -> bool:
        """Indicates if an asyncio task is currently executing `run()`."""
        return self._run_task is not None and not self._run_task.done()

    # Handler hooks

    def setup(self):
        for event in ("start", "pause", "resume", "stop"):
            self.register(event)

    def teardown(self):
        if self.is_running():
            self._run_task.cancel()

    def hook(self, event: str, *args):
        if event in ("start", "resume"):
            if not self.is_running():
                self._run_task = asyncio.create_task(self.run())

            # Setting internal origin here is only useful for the resume event;
            # the run task must manually do this regardless
            self.internal_origin = self.time
        elif event == "pause":
            self.env.time.origin = self.time
        elif event == "stop":
            self.env.time.origin = self.time
            self.teardown()
