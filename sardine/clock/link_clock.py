from typing import Optional, Union

import link
import math
from time import time

from ..base import BaseClock, BaseThreadedLoopMixin

NUMBER = Union[int, float]

__all__ = ("LinkClock",)


class LinkClock(BaseThreadedLoopMixin, BaseClock):
    def __init__(
        self,
        tempo: NUMBER = 120,
        bpb: int = 4,
        loop_interval: float = 0.001,
    ):
        super().__init__(loop_interval=loop_interval)

        self._link: Optional[link.Link] = None
        self._tick: int = 0
        self._beat: int = 0
        self._beat_duration: float = 0.0
        self._beats_per_bar: int = bpb
        self._internal_origin: float = 0.0
        self._internal_time: float = 0.0
        self._last_capture: Optional[link.SessionState] = None
        self._phase: float = 0.0
        self._playing: bool = False
        self._tempo: float = float(tempo)
        self._tidal_nudge: int = 0
        self._link_time: int = 0
        self._beats_per_cycle: int = 4
        self._framerate: float = 1 / 20

    ## VORTEX   ################################################

    def get_cps(self) -> int | float:
        """Get the BPM in cycles per second (Tidal approach to time)"""
        return self.tempo / self._beats_per_bar / 60.0

    @property
    def cps(self) -> int | float:
        """Return the current cps"""
        return self.get_cps()

    @property
    def tick(self) -> int | float:
        """Return the current clock tick"""
        return self._tick

    @tick.setter
    def tick(self, value: int) -> None:
        """Set the current clock tick"""
        self._tick = value

    @cps.setter
    def cps(self, value: int | float) -> None:
        self.tempo = value * self._beats_per_bar * 60.0

    @property
    def bps(self) -> int | float:
        """Return the number of beats that can fit into a second"""
        return 1.0 / self.beat_duration

    def beatAtTime(self, time: int | float) -> float:
        """Equivalent to Ableton Link beatAtTime method"""
        return (time - self.internal_origin) * self.bps

    def timeAtBeat(self, beat: float) -> float:
        """Equivalent to Ableton Link timeAtBeat method"""
        return self.internal_origin + (self.beat / self.bps)

    # def _notify_tidal_streams(self):
    #     """
    #     Notify Tidal Streams of the current passage of time.
    #     """
    #     self.tick += 1

    #     # Logical time since the clock started ticking: sum of frames
    #     logical_now, logical_next = (
    #         self.internal_origin + (self.tick * self._framerate),
    #         self.internal_origin + ((self.tick + 1) * self._framerate),
    #     )

    #     # Current time (needed for knowing wall clock time)
    #     now = self.shifted_time + self._tidal_nudge

    #     # Wall clock time for the "ideal" logical time
    #     cycle_from, cycle_to = (
    #         self.beatAtTime(logical_now) / (self.beats_per_bar * 2),
    #         self.beatAtTime(logical_next) / (self.beats_per_bar * 2),
    #     )

    #     # Sending to each individual subscriber for scheduling using timestamps
    #     try:
    #         for sub in self.env._vortex_subscribers:
    #             sub.notify_tick(
    #                 clock=self,
    #                 cycle=(cycle_from, cycle_to),
    #                 cycles_per_second=self.cps,
    #                 beats_per_cycle=(self.beats_per_bar * 2),
    #                 now=now,
    #             )
    #     except Exception as e:
    #         print(e)

    ## GETTERS  ################################################

    @property
    def bar(self) -> int:
        return self.beat // self.beats_per_bar

    @property
    def beat(self) -> int:
        return self._beat + int(self.beat_shift)

    @property
    def beat_duration(self) -> float:
        return self._beat_duration

    @property
    def beat_shift(self) -> float:
        """A shorthand for time shift expressed in number of beats."""
        return self.env.time.shift / self.beat_duration

    @property
    def beats_per_bar(self) -> int:
        return self._beats_per_bar

    @property
    def internal_origin(self) -> float:
        return self._internal_origin

    @property
    def internal_time(self) -> float:
        return self._internal_time

    @property
    def phase(self) -> float:
        return (self._phase + self.beat_shift) % self.beat_duration

    @property
    def tempo(self) -> float:
        return self._tempo

    ## SETTERS  ##############################################################

    @beats_per_bar.setter
    def beats_per_bar(self, bpb: int):
        self._beats_per_bar = bpb

    @internal_origin.setter
    def internal_origin(self, origin: float):
        self._internal_origin = origin

    @tempo.setter
    def tempo(self, new_tempo: float) -> None:
        if self._link is not None:
            session = self._link.captureSessionState()
            session.setTempo(new_tempo, self.beats_per_bar)
            self._link.commitSessionState(session)

    ## METHODS  ##############################################################

    def _capture_link_info(self):
        s: link.SessionState = self._link.captureSessionState()
        self._last_capture = s
        self._link_time: int = self._link.clock().micros()
        beat: float = s.beatAtTime(self._link_time, self.beats_per_bar)
        phase: float = s.phaseAtTime(self._link_time, self.beats_per_bar)
        playing: bool = s.isPlaying()
        tempo: float = s.tempo()

        self._internal_time = self._link_time / 1_000_000
        self._beat = int(beat)
        self._beat_duration = 60 / tempo
        # Sardine phase is typically defined from 0.0 to the beat duration.
        # Conversions are needed for the phase coming from the LinkClock.
        self._phase = phase % 1 * self.beat_duration
        self._playing = playing
        self._tempo = tempo

    def before_loop(self):
        self._link = link.Link(self._tempo)
        self._link.enabled = True
        self._link.startStopSyncEnabled = True

        # Set the origin at the start
        self._capture_link_info()
        self._internal_origin = self.internal_time

    def loop(self):
        self._capture_link_info()

    def after_loop(self):
        self._link = None
