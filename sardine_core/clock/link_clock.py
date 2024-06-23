from typing import Optional

import link

from sardine_core.base import BaseClock, BaseThreadedLoopMixin

NUMBER = int | float

__all__ = ("LinkClock",)

DEBUG = False


class LinkClock(BaseThreadedLoopMixin, BaseClock):
    def __init__(
        self,
        tempo: NUMBER = 120,
        bpb: int = 4,
        loop_interval: float = 0.001,
        startup_delay: float = 3.0,
    ):
        super().__init__(loop_interval=loop_interval)

        self.startup_delay = startup_delay

        self._link: Optional[link.Link] = None
        self._tick: int = 0
        self._beat: int = 0
        self._beat_duration: float = 0.0
        self._beats_per_bar: int = bpb
        self._internal_origin: float = 0.0
        self._internal_time: float = 0.0
        self._last_capture: Optional[link.SessionState] = None
        self._phase: float = 0.0
        self._link_phase: float = 0.0
        self._playing: bool = False
        self._tempo: float = float(tempo)
        self._tidal_nudge: int = 0
        self._link_time: int = 0
        self._beats_per_cycle: int = 4
        self._framerate: float = 1 / 20
        self._paused_link_phase: float = 0.0
        self._time_shift: float = 0.0
        self._synced: bool = False
        self._startup_time: float = 0.0

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

    ## GETTERS  ################################################

    @property
    def bar(self) -> int:
        try:
            return self.beat // self.beats_per_bar
        except ZeroDivisionError:
            return 0

    @property
    def beat(self) -> int:
        return self._beat + int(self.beat_shift)

    @beat.setter
    def beat(self, beat: int) -> None:
        self._last_capture.requestBeatAtTime(beat, self._link_time, self.beats_per_bar)
        self._link.commitSessionState(self._last_capture)
        self.env.dispatch("reset_iterator", 0)

    @property
    def beat_duration(self) -> float:
        return self._beat_duration

    @property
    def beat_shift(self) -> float:
        """A shorthand for time shift expressed in number of beats."""
        try:
            return self.env.time.shift / self.beat_duration
        except ZeroDivisionError:
            return 0

    @property
    def beats_per_bar(self) -> int:
        return self._beats_per_bar

    @property
    def internal_origin(self) -> float:
        if not self._synced:
            return 0.0

        return self._internal_origin

    @property
    def internal_time(self) -> float:
        if not self._synced:
            return 0.0

        return self._internal_time + self._time_shift

    @property
    def phase(self) -> float:
        try:
            return (self._phase + self.beat_shift) % self.beat_duration
        except ZeroDivisionError:
            return 0.0

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
        self.env.dispatch("tempo_change", self.tempo, new_tempo)
        if self._link is not None:
            session = self._link.captureSessionState()
            session.setTempo(new_tempo, self._link_time)
            self._link.commitSessionState(session)

    ## METHODS  ##############################################################

    def _capture_link_info(self, *, update_transport: bool):
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
        self._link_phase = phase
        self._phase = phase % 1 * self.beat_duration
        self._playing, last_playing = playing, self._playing
        self._tempo = tempo

        if update_transport:
            if playing and not last_playing:
                self.env.resume()
            elif not playing and last_playing:
                self.env.pause()

    def before_loop(self):
        self._time_shift = 0.0
        self._synced = False

        self._link = link.Link(self._tempo)
        self._link.enabled = True
        self._link.startStopSyncEnabled = True

        # Record the initial time so we know how long to wait before syncing
        self._capture_link_info(update_transport=False)
        self._startup_time = self._internal_time

    def loop(self):
        self._capture_link_info(update_transport=True)

        # Give Link some time to sync before we start reporting time.
        # Make sure the origin starts at phase 0.
        if (
            not self._synced
            and self._internal_time - self._startup_time >= self.startup_delay
        ):
            phase_time = self._link_phase * self.beat_duration
            self._internal_origin = self._internal_time - phase_time
            self._synced = True

        if (
            DEBUG
            and getattr(self, "_pause_check", False)
            and self.time >= self._pause_state[0]
        ):
            self._pause_check = False
            pause_time, pause_phase = self._pause_state
            deviation = self._link_phase - pause_phase
            print(
                f"({pause_time:.3f}, {pause_phase:.3f}) -> "
                f"({self.time:.3f}, {self._link_phase:.3f}), "
                f"{deviation = :.3f}"
            )

    def after_loop(self):
        self._link = None

    def hook(self, event: str, *args):
        super().hook(event, *args)

        if self._link is None:
            return
        elif event == "pause":
            # Remember the current phase so the next time the clock is resumed,
            # we can rewind time so the phase appears continuous.
            self._paused_link_phase = self._link_phase

            if DEBUG:
                self._pause_check = False
                self._pause_state = (self.time, self._link_phase)

        elif event == "resume":
            # Alternative formula: (-bpb + lp - plp) % -bpb
            delta = (self._link_phase - self._paused_link_phase) % self.beats_per_bar
            if delta > 0:
                # Don't allow time to jump forward, rewind instead.
                delta -= self.beats_per_bar

            if DEBUG:
                self._pause_check = True
                print(f"Time shifting by: {delta * self.beat_duration:.3f}")

            self._time_shift += delta * self.beat_duration

        if self._last_capture is not None:
            # Allow boradcasting start/stop from sardine transport methods.
            # This will cause a second pause/resume call from _capture_link_info(),
            # but Sardine's transport methods are idempotent so it should be fine.
            if event == "pause" and self._playing:
                self._last_capture.setIsPlaying(False, self._link_time)
                self._link.commitSessionState(self._last_capture)
            elif event == "resume" and not self._playing:
                self._last_capture.setIsPlaying(True, self._link_time)
                self._link.commitSessionState(self._last_capture)
                self.beat = 0
