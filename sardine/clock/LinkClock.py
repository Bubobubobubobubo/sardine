from ..base.BaseClock import BaseClock
from typing import TYPE_CHECKING
from time import perf_counter
import asyncio
import link

if TYPE_CHECKING:
    from ..FishBowl import FishBowl

class LinkClock(BaseClock):

    def __init__(self, env: 'FishBowl', tempo: float = 120):
        self._alive = asyncio.Event()
        self._resumed = asyncio.Event()
        self._resumed.set()
        self._env = env
        self._time = env._time
        self._tempo = tempo
        self._link = link.Link(self.tempo)
        self._linktime = {
            "tempo": 0,
            "beats": 0,
            "phase": 0
        }

    ## GETTERS  ############################################################## 

    @property
    def phase(self) -> int:
        """The phase of the current beat in ticks."""
        return self.tick % self.ppqn

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
            beats_str = s.beatAtTime(link_time, self.beat_per_bar)
            playing_str = str(s.isPlaying())
            phase = s.phaseAtTime(link_time, self.beat_per_bar)
            return {
                "tempo": tempo_str,
                "beats": beats_str,
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