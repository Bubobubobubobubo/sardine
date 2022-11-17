from time import monotonic_ns
from typing import TYPE_CHECKING, Union
import asyncio
from ..base.handler import BaseHandler

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

NUMBER = Union[int, float]

class Clock(BaseHandler):

    def __init__(self, env: 'FishBowl',
                 time: NUMBER,
                 time_shift: NUMBER,
                 tempo: NUMBER = 120,
                 bpb: int = 4):
        self._type = "InternalClock"
        self._alive = asyncio.Event()
        self._resumed = asyncio.Event()
        self._env = env

        # Time related attributes
        self.time = time
        self.time_shift = time_shift
        self._tempo = tempo
        self._beats_per_bar = bpb
        self.origin = monotonic_ns()

        # Possible event types
        self._events = {
            'start': self._start,
            'stop': self._stop,
            'pause': self._pause,
            'resume': self._resume,
        }

    ## REPR AND STR ############################################################

    def __repr__(self) -> str:
        return f"({self._type}, Tempo: {self._tempo}) -> Beat: {self.beat:1f}, Bar: {self.bar:1f}, Phase: {self.phase:1f}"

    #### GETTERS  ############################################################

    @property
    def beat(self) -> int:
        """Actual beat on the clock.

        Returns:
            int: Beat
        """
        return self.time() / self.beat_duration

    @property
    def current_beat(self) -> int:
        return self.beat // self._beats_per_bar

    @property
    def bar(self) -> int:
        return self.beat / self._beats_per_bar

    @property
    def beat_duration(self) -> float:
        return 60 / self._tempo

    @property
    def phase(self) -> float:
        """Actual time between beginning of bar and next bar

        Returns:
            float: phase
        """
        return self.time() % self._beats_per_bar

    @property
    def bpm(self) -> float:
        """Current beats per minute

        Returns:
            float: bpm
        """
        return self._tempo

    @property
    def tempo(self) -> float:
        """Current tempo

        Returns:
            float: tempo
        """
        return self._tempo

    @property
    def beats_per_bar(self) -> int:
        """Number of beats per bar

        Returns:
            int: beats per bar
        """
        return self._beats_per_bar

    #### SETTERS ############################################################

    @bpm.setter
    def bpm(self, bpm: float):
        """Beats per minute. Tempo for the Internal Sardine Clock.

        Args:
            bpm (float): new tempo value

        Raises:
            ValueError: if tempo < 1 or tempo > 999 (non-musical values)
        """
        if not 1 <= bpm <= 999:
            raise ValueError("bpm must be within 1 and 999")
        self._tempo = bpm

    @tempo.setter
    def tempo(self, tempo: float):
        """Beats per minute. Tempo for the Internal Sardine Clock.

        Args:
            tempo (float): new tempo value

        Raises:
            ValueError: if tempo < 1 or tempo > 999 (non-musical values)
        """
        if not 1 <= tempo <= 999:
            raise ValueError("bpm must be within 1 and 999")
        self._tempo = tempo

    ## METHODS  ##############################################################

    def setup(self):
        for event in self._events:
            self.register(event)

    def hook(self, event: str, *args):
        func = self._events[event]
        func(*args)

    def time(self) -> int:
        """
        Get current time in monotonic nanoseconds (best possible resolution)
        without approximation due to float conversion.
        """
        return (monotonic_ns() - self.origin) / 1_000_000_000

    def is_running(self) -> bool:
        """Return a boolean indicating if the clock is currently running.

        Returns:
            bool: running
        """
        return self._alive.is_set()

    def is_paused(self) -> bool:
        """Return a boolean indicating is the clock is currently paused or not.

        Returns:
            bool: paused?
        """
        return False if self._resumed.is_set() else True

    def _start(self):
        """This method is used to enter the clock run() main loop."""
        self._alive.set()
        asyncio.create_task(self.run())

    def _pause(self):
        """Pausing the internal clock. Use resume() to continue."""
        if self._resumed.is_set():
            self._resumed.clear()

    def _resume(self):
        """Resuming the internal clock. Use pause() for the opposite."""
        if not self._resumed.is_set():
            self._resumed.set()

    def _stop(self):
        """Stop the internal clock. End the internal run() main loop."""
        self._alive.clear()


    async def time_shift(self):
        pass

    async def run(self):
        """
        Main loop for the internal clock. This method is just implemented in
        compliance with the base clock. Strictly speaking, this method is 
        doing nothing.
        """
        while True:
            await self._resumed.wait()
            if self._alive.is_set():
                await asyncio.sleep(0.0)
            else:
                return
