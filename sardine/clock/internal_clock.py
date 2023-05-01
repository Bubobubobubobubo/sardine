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
        self.beats_per_bar = bpb
        self._internal_origin = 0.0
        self._tidal_nudge: float = 0.0
        self._framerate = 1/20
        self._start: float = time.time()

    #### VORTEX  #############################################################

    def get_cps(self) -> int|float:
        """Get the BPM in cycles per second (Tidal approach to time)"""
        return self.tempo / self._beats_per_bar / 60.0


    @property
    def beats_per_cycle(self) -> int|float:
        return self.beats_per_bar

    @property
    def cps(self) -> int|float:
        """Return the current cps"""
        return self.get_cps()

    @cps.setter
    def cps(self, value: int|float) -> None:
        self.tempo = value * self._beats_per_bar * 60.0

    def _notify_tidal_streams(self):
        """
        Notify Tidal Streams of the current passage of time.
        """

        cycle_factor = self.beat_duration / self.beats_per_bar
        time = self.shifted_time + self._tidal_nudge

        cycle_from, cycle_to = (
                time / cycle_factor,
                (time / cycle_factor) + self._framerate
        )
        time_on, time_off = (
                cycle_from * cycle_factor,
                cycle_to * cycle_factor
        )

        try:
            for sub in self.env._vortex_subscribers:
                sub.notify_tick(
                        cycle=(cycle_from, cycle_to),
                        info=(time_on, time_off),
                        cycles_per_second=self.cps,
                        beats_per_cycle=self.beats_per_cycle,
                        now=time)
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
