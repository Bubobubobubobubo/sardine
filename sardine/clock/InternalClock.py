from ..base.clock import BaseClock
from typing import TYPE_CHECKING, Union
from time import perf_counter, monotonic_ns
import asyncio

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

class Clock(BaseClock):

    """
    Basic Internal Clock. This clock is the default Clock Sardine will try to use.
    It is preferably used when playing alone, as it is not capable of synchronising
    to anything. For MIDI synchronisation, schedule a MIDI Clock message.

    The clock is exposing a few methods to the users:

    - start(): start the internal clock loop.
    - stop(): stop the internal clock loop.
    - pause(): pause.
    - resume(): unpause.
    - sleep(): ???.

    You can set the tempo and the number of beats per bar by tweaking 
    the respective attributes:

    clock.bpm / clock.tempo = 124
    clock.beats_per_bar = 8
    """

    def __init__(self, env: 'FishBowl', tempo: float = 120, bpb: int = 4):
        """Basic internal clock

        Args:
            env (FishBowl): Environment for dispatching information
            time (Time): Flow of time
            tempo (float, optional): Beats per minute (tempo). Defaults to 120.
            bpb (int, optional): Number of beats per bar. Defaults to 4.
        """
        self._type = "InternalClock"
        self._alive = asyncio.Event()
        self._resumed = asyncio.Event()
        self._resumed.set()
        self._env = env
        self._tempo = tempo
        self._beats_per_bar = bpb
        self._origin = monotonic_ns()

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
            ValueError: if tempo < 20 or tempo > 999 (non-musical values)
        """
        if not 20 < bpm < 999:
            raise ValueError("bpm must be within 1 and 800")
        self._tempo = bpm

    @tempo.setter
    def tempo(self, tempo: float):
        """Beats per minute. Tempo for the Internal Sardine Clock.

        Args:
            tempo (float): new tempo value

        Raises:
            ValueError: if tempo < 20 or tempo > 999 (non-musical values)
        """
        if not 20 < tempo < 999:
            raise ValueError("bpm must be within 1 and 800")
        self._tempo = tempo

    ## METHODS  ##############################################################

    def time(self) -> int:
        """
        Get current time in monotonic nanoseconds (best possible resolution)
        without approximation due to float conversion.
        """
        return (monotonic_ns() - self._origin) / 1_000_000_000

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

    def start(self):
        """This method is used to enter the clock run() main loop."""
        self._alive.set()
        asyncio.create_task(self.run())

    def pause(self):
        """Pausing the internal clock. Use resume() to continue."""
        if self._resumed.is_set():
            self._resumed.clear()

    def resume(self):
        """Resuming the internal clock. Use pause() for the opposite."""
        if not self._resumed.is_set():
            self._resumed.set()

    def stop(self):
        """Stop the internal clock. End the internal run() main loop."""
        self._alive.clear()

    async def sleep(self, duration: Union[int, float]):
        """Sleep for a given time duration"""
        await asyncio.sleep(duration)

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