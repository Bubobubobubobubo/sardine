from time import monotonic_ns
from typing import Union
import asyncio
from ..base.handler import BaseHandler

NUMBER = Union[int, float]


class Clock(BaseHandler):

    def __init__(
        self,
        tempo: NUMBER = 120,
        bpb: int = 4,
    ):
        super().__init__()
        self._type = "InternalClock"

        # Time related attributes
        self._tempo = tempo
        self._beats_per_bar = bpb

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

    def time(self) -> int:
        """
        Get current time in monotonic nanoseconds (best possible resolution)
        without approximation due to float conversion.
        """
        return (monotonic_ns() - self.origin) / 1_000_000_000

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
