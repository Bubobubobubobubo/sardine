import asyncio
import threading
import time
from typing import Optional, Union

import link

from ..base import BaseClock

NUMBER = Union[int, float]

__all__ = ("LinkClock",)


class LinkClock(BaseClock):

    POLL_INTERVAL = 0.001

    def __init__(
        self,
        tempo: NUMBER = 120,
        bpb: int = 4,
    ):
        super().__init__()

        self._link: Optional[link.Link] = None
        self._beat: int = 0
        self._beat_duration: float = 0.0
        self._beats_per_bar: int = bpb
        self._internal_origin: float = 0.0
        self._internal_time: float = 0.0
        self._phase: float = 0.0
        self._playing: bool = False
        self._tempo: float = float(tempo)

        # Thread control
        self._run_thread: Optional[threading.Thread] = None
        self._completed_event = asyncio.Event()

    ## GETTERS  ################################################

    @property
    def bar(self) -> int:
        return self.beat // self.beats_per_bar

    @property
    def beat(self) -> int:
        return self._beat

    @property
    def beat_duration(self) -> float:
        return self._beat_duration

    @property
    def beats_per_bar(self) -> int:
        return self._beats_per_bar

    @property
    def internal_time(self) -> float:
        return self._internal_time

    @property
    def internal_origin(self) -> float:
        return self._internal_origin

    @property
    def phase(self) -> float:
        return self._phase

    @property
    def tempo(self) -> float:
        return self._tempo

    ## SETTERS  ##############################################################

    @beats_per_bar.setter
    def beats_per_bar(self, bpb: int):
        self._beats_per_bar = bpb

    @tempo.setter
    def tempo(self, new_tempo: float) -> None:
        if self._link is not None:
            session = self._link.captureSessionState()
            session.setTempo(new_tempo, self.beats_per_bar)
            self._link.commitSessionState(session)

    ## METHODS  ##############################################################

    def _capture_link_info(self):
        s: link.SessionState = self._link.captureSessionState()
        link_time: int = self._link.clock().micros()
        beat: float    = s.beatAtTime(link_time, self.beats_per_bar)
        phase: float   = s.phaseAtTime(link_time, self.beats_per_bar)
        playing: bool  = s.isPlaying()
        tempo: float   = s.tempo()

        self._internal_time = link_time / 1_000_000
        self._beat = int(beat)
        self._beat_duration = 60 / tempo
        self._phase = phase / self.beats_per_bar
        self._playing = playing
        self._tempo = tempo

    def _run(self):
        try:
            self._link = link.Link(self._tempo)

            # Set the origin at the start
            self._capture_link_info()
            self._internal_origin = self.internal_time

            # Poll continuously to get the latest time
            while not self._completed_event.is_set():
                self._capture_link_info()
                time.sleep(self.POLL_INTERVAL)
        finally:
            self._link = None
            self._completed_event.set()

    async def run(self):
        """Main loop for the LinkClock"""
        self._completed_event.clear()
        self._run_thread = threading.Thread(target=self._run)
        self._run_thread.start()

        try:
            await self._completed_event.wait()
        finally:
            self._completed_event.set()
