from ..base.BaseClock import BaseClock
from typing import TYPE_CHECKING
from time import perf_counter
import asyncio
import link

if TYPE_CHECKING:
    from ..FishBowl import FishBowl

class LinkClock(BaseClock):

    def __init__(self, env: 'FishBowl', tempo: float = 120, bpb: int = 4):
        self._alive = asyncio.Event()
        self._resumed = asyncio.Event()
        self._resumed.set()
        self._env = env
        self._time = env.time
        self._time_grain = 0.01
        self._beats_per_bar = bpb
        self._drift = 0.0
        self._tempo = tempo
        self._link = link.Link(self._tempo)
        self._linktime = {
            "tempo": 0,
            "beat": 0,
            "phase": 0
        }

    ## REPR AND STR ############################################################ 

    def __repr__(self) -> str:
        el = self._time._elapsed_time
        return f"{el:1f} -> [{self.tempo}|{self.bar:1f}: {int(self.phase)}/{self._beats_per_bar}] (Drift: {self.drift})"

    ## GETTERS  ################################################

    @property
    def drift(self) -> float:
        """Drift compensation for the waiting mechanism

        Returns:
            float: drift amount on last cycle
        """
        return self._drift

    @property
    def bar(self) -> int:
        return self.beat / self._beats_per_bar

    @property
    def time_grain(self) -> int:
        """Return the smallest unity of time used by the clock """
        return self._time_grain

    @property
    def phase(self) -> int:
        """The phase of the current beat in ticks."""
        return self._linktime['phase']

    @property
    def beat(self) -> int:
        """Current beat"""
        return self._linktime['beat']

    @property
    def tempo(self) -> int:
        """The phase of the current beat in ticks."""
        return self._linktime['tempo']

    @property
    def bpm(self) -> int:
        """The phase of the current beat in ticks."""
        return self._linktime['tempo']

    @property
    def linktime(self) -> dict:
        """Return current Link clock time"""
        return self._linktime

    ## SETTERS  ############################################################## 

    @linktime.setter
    def linktime(self, new_time: dict) -> None:
        self._linktime = self._get_new_linktime(new_time)

    ## METHODS  ############################################################## 

    def _capture_link_info(self) -> dict:
        """Capture information about the current state of the Link session. 
        Returns:
            dict: a dictionnary containing temporal information 
            about the Link session.
        """
        if self._link:
            s = self._link.captureSessionState()
            link_time = self._link.clock().micros()
            tempo_str = s.tempo()
            beats_str = s.beatAtTime(link_time, self._beats_per_bar)
            playing_str = str(s.isPlaying())
            phase = s.phaseAtTime(link_time, self._beats_per_bar)
            return {
                "tempo": tempo_str,
                "beat": beats_str,
                "playing": playing_str,
                "phase": phase,
            }

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
        self._link.enabled = True
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

    async def run(self):
        """Main loop for the LinkClock"""
        self._drift = 0.0
        while True:
            await self._resumed.wait()
            if self._alive.is_set():
                begin = perf_counter()
                await asyncio.sleep(0.0)
                self._linktime = self._capture_link_info()
                self._time._elapsed_time += self._time_grain
                self._env.dispatch('tick')
                self._drift = perf_counter() - begin
            else:
                return