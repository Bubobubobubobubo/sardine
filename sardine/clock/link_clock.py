from typing import Optional, Union

import link
import math

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
        self._beat: int = 0
        self._beat_duration: float = 0.0
        self._beats_per_bar: int = bpb
        self._internal_origin: float = 0.0
        self._internal_time: float = 0.0
        self._last_capture: Optional[link.SessionState] = None
        self._start: float = 0.0
        self._phase: float = 0.0
        self._playing: bool = False
        self._tempo: float = float(tempo)
        self._subscribers = []
        self._ticks: int = 0
        self._frame_rate = 1000000 * 1/20
        self._beats_per_cycle: int = 4

    ## VORTEX   ################################################

    def subscribe(self, subscriber):
        """Subscribe an object to tick notifications"""
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        """Unsubscribe from tick notifications"""
        self._subscribers.remove(subscriber)

    def _notify_tidal_streams(self):
        """
        Notify Tidal Streams of the current passage of time.
        """

        start_beat = self._link.captureSessionState().beatAtTime(self._start, 4)

        # FIXME rate, bpc and latency should be constructor parameters
        self._ticks += 1

        logical_now = math.floor(self._start + (self._ticks * self._frame_rate))
        logical_next = math.floor(self._start + ((self._ticks + 1) * self._frame_rate))

        now = self._link.clock().micros()

        wait = (logical_now - now) / mill


        s = self._last_capture
        cps = (s.tempo() / self._beats_per_cycle) / 60
        cycle_from = s.beatAtTime(logical_now, 0) / self._beats_per_cycle
        cycle_to = s.beatAtTime(logical_next, 0) / self._beats_per_cycle

        try:
            for sub in self._subscribers:
                sub.notify_tick((cycle_from, cycle_to), s, cps, bpc, mill, now)
        except:
            pass

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
        link_time: int = self._link.clock().micros()
        beat: float = s.beatAtTime(link_time, self.beats_per_bar)
        phase: float = s.phaseAtTime(link_time, self.beats_per_bar)
        playing: bool = s.isPlaying()
        tempo: float = s.tempo()

        self._internal_time = link_time / 1_000_000
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
        self._start = self._link.clock().micros()

        # Set the origin at the start
        self._capture_link_info()
        self._internal_origin = self.internal_time

    def loop(self):
        self._capture_link_info()

    def after_loop(self):
        self._link = None
