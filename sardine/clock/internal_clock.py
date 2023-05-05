import asyncio
import math
import time
from typing import Union

from ..base import BaseClock

NUMBER = Union[int, float]

__all__ = ("InternalClock",)


class InternalClock(BaseClock):
    def __init__(
        self,
        tempo: NUMBER = 120,
        bpb: int = 4,
    ):
        super().__init__()
        self.tempo = tempo
        self._tick: int = 0
        self.beats_per_bar = bpb
        self._internal_origin = 0.0
        self._tidal_nudge: float = 0.0
        self._framerate = 1 / 20
        self._start: float = time.time()

    #### VORTEX  #############################################################

    def get_cps(self) -> int | float:
        """Get the BPM in cycles per second (Tidal approach to time)"""
        return self.tempo / self._beats_per_bar / 60.0

    @property
    def tick(self) -> int | float:
        """Return the current clock tick"""
        return self._tick

    @tick.setter
    def tick(self, value: int) -> None:
        """Set the current clock tick"""
        self._tick = value

    @property
    def beats_per_cycle(self) -> int | float:
        return self.beats_per_bar

    @property
    def cps(self) -> int | float:
        """Return the current cps"""
        return self.get_cps()

    @cps.setter
    def cps(self, value: int | float) -> None:
        self.tempo = value * self._beats_per_bar * 60.0

    @property
    def bps(self) -> int|float:
        """Return the number of beats that can fit into a second"""
        return 1.0 / self.beat_duration

    def beatAtTime(self, time: int|float) -> float:
        """Equivalent to Ableton Link beatAtTime method"""
        return (time - self.internal_origin) * self.bps

    def timeAtBeat(self, beat: float) -> float:
        """Equivalent to Ableton Link timeAtBeat method"""
        return self.internal_origin + (self.beat / self.bps)


    def _notify_tidal_streams(self):
        """
        Notify Tidal Streams of the current passage of time.
        """
        self.tick += 1

        # Logical time since the clock started ticking: sum of frames
        logical_now, logical_next = (
            self.internal_origin + (self.tick * self._framerate),
            self.internal_origin + ((self.tick + 1) * self._framerate),
        )

        # Current time (needed for knowing wall clock time)
        now = self.shifted_time + self._tidal_nudge

        # Wall clock time for the "ideal" logical time 
        cycle_from, cycle_to = (
                self.beatAtTime(logical_now) / (self.beats_per_bar * 2),
                self.beatAtTime(logical_next) / (self.beats_per_bar * 2),
        )

        # Sending to each individual subscriber for scheduling using timestamps
        try:
            for sub in self.env._vortex_subscribers:
                sub.notify_tick(
                    clock=self,
                    cycle=(cycle_from, cycle_to),
                    cycles_per_second=self.cps,
                    beats_per_cycle=(self.beats_per_bar * 2),
                    now=now,
                )
        except Exception as e:
            print(e)


    #### GETTERS  ############################################################

    @property
    def bar(self) -> int:
        return self.beat // self.beats_per_bar

    @property
    def beat(self) -> int:
        # FIXME: Internal clock beat will abruptly change with tempo
        return int(self.shifted_time // self.beat_duration)

    @property
    def beat_duration(self) -> float:
        return self._beat_duration

    @property
    def beats_per_bar(self) -> int:
        return self._beats_per_bar

    @property
    def internal_origin(self) -> float:
        return self._internal_origin

    @property
    def internal_time(self) -> float:
        return time.perf_counter()

    @property
    def phase(self) -> float:
        return self.shifted_time % self.beat_duration

    @property
    def tempo(self) -> float:
        return self._tempo

    #### SETTERS ############################################################

    @beats_per_bar.setter
    def beats_per_bar(self, bpb: int):
        self._beats_per_bar = bpb

    @internal_origin.setter
    def internal_origin(self, origin: float):
        self._internal_origin = origin

    @tempo.setter
    def tempo(self, new_tempo: NUMBER):
        new_tempo = float(new_tempo)

        if not 1 <= new_tempo <= 999:
            raise ValueError("new tempo must be within 1 and 999")

        self._tempo = new_tempo
        self._beat_duration = 60 / new_tempo

    ## METHODS  ##############################################################

    async def sleep(self, duration: Union[float, int]) -> None:
        return await asyncio.sleep(duration)

    async def run(self):
        # The internal clock simply uses the system's time
        # so we don't need to do any polling loop here
        self._internal_origin = self.internal_time
        await asyncio.sleep(math.inf)
