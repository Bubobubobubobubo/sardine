from abc import ABC, abstractmethod
import asyncio
from typing import Optional, Union

from .handler import BaseHandler

__all__ = ("BaseClock",)


class BaseClock(BaseHandler, ABC):
    """The base for all clocks to inherit from.

    This interface expects clocks to manage its own source of time
    and provide the `phase`, `beat`, and `tempo` properties.

    In addition, an optional `async sleep()` method can be defined
    to provide a mechanism for sleeping a specified duration.
    If this method is not defined, the `FishBowl.sleeper` instance
    will use a built-in polling mechanism for sleeping.
    """

    def __init__(self):
        super().__init__()
        self._run_task: Optional[asyncio.Task] = None
        self._true_time_is_origin: bool = True

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
    def beat_duration(self) -> float:
        """The length of a single beat in seconds.

        Typically this is represented as the function `60 / tempo`.
        """

    @property
    @abstractmethod
    def beats_per_bar(self) -> int:
        """The number of beats in each bar."""

    @property
    @abstractmethod
    def internal_origin(self) -> Optional[float]:
        """The clock's internal time origin if available, measured in seconds.

        At the start of the `run()` method, this should be set as early
        as possible in order for the `time` property to compute the
        elapsed time.

        This **must** support a setter as the base clock will automatically
        set this to the `internal_time` when the fish bowl is resumed.
        """

    @property
    @abstractmethod
    def internal_time(self) -> Optional[float]:
        """The clock's internal time if available, measured in seconds.

        This attribute should be continuously updated when the
        clock starts so the `time` property is able to move forward.
        """

    @property
    @abstractmethod
    def phase(self) -> float:
        """The phase of the current beat in the range `[0, beat_duration)`."""

    @property
    @abstractmethod
    def tempo(self) -> float:
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
        are not available, i.e. been set to `None`, this will default
        to the `Time.origin` (still including time shift). This should
        ideally be avoided when the clock starts running so time can
        flow as soon as possible.
        """
        return self.true_time + self.env.time.shift

    @property
    def true_time(self) -> float:
        """A variant of `time` except that no time shift is applied."""
        if self._true_time_is_origin:
            return self.env.time.origin

        i_time, i_origin = self.internal_time, self.internal_origin
        if i_time is None or i_origin is None:
            return self.env.time.origin

        return i_time - i_origin + self.env.time.origin

    # Public methods

    def can_sleep(self) -> bool:
        """Checks if the clock supports sleeping."""
        return getattr(self, "sleep", None) is not BaseClock.sleep

    def get_beat_time(self, n_beats: Union[int, float], *, sync: bool = True) -> float:
        """Determines the amount of time to wait for N beats to pass.

        Args:
            n_beats (Union[int, float]): The number of beats to wait for.
            sync (bool):
                If True, the clock's current phase is subtracted from
                the initial duration to synchronize with the clock beat.
                If False, no synchronization is done.

        Returns:
            float: The amount of time to wait in seconds.
        """
        interval = self.beat_duration * n_beats
        if interval <= 0.0:
            return 0.0
        elif not sync:
            return interval

        return interval - self.phase % interval

    def get_bar_time(self, n_bars: Union[int, float], *, sync: bool = True) -> float:
        """Determines the amount of time to wait for N bars to pass.

        Args:
            n_bars (Union[int, float]): The number of bars to wait for.
            sync (bool):
                If True, the clock's current phase is subtracted from
                the initial duration to synchronize with the clock beat.
                If False, no synchronization is done.

        Returns:
            float: The amount of time to wait in seconds.

        """
        return self.get_beat_time(n_bars * self.beats_per_bar, sync=sync)

    def is_running(self) -> bool:
        """Indicates if an asyncio task is currently executing `run()`."""
        return self._run_task is not None and not self._run_task.done()

    async def sleep(self, duration: Union[float, int]) -> None:
        """Sleeps for the given duration.

        This method can be optionally overridden by subclasses.
        If it is not overridden, it is assumed that the class
        does not support sleeping.

        Any implementations of this sleep must be able to handle
        `asyncio.CancelledError` on any asynchronous statements.
        """
        raise NotImplementedError

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

            # Setting internal origin here is only useful for the resume event,
            # unless the clock is able to provide an internal time before
            # the clock has started
            self.internal_origin = self.internal_time
            self._true_time_is_origin = False
        elif event == "pause":
            self.env.time.origin = self.true_time
            self._true_time_is_origin = True
        elif event == "stop":
            self.env.time.origin = self.true_time
            self._true_time_is_origin = True
            self.teardown()
        # print(f"{event=} {self.env.time.origin=} {self.true_time=} "
        #       f"{self.env.is_paused()=} {self.env.is_running()=}")
