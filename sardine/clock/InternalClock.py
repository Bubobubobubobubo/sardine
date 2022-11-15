from ..base.BaseClock import BaseClock
from typing import TYPE_CHECKING
from time import perf_counter
import asyncio

if TYPE_CHECKING:
    from ..FishBowl import FishBowl
    from .Time import Time

class Clock(BaseClock):

    def __init__(self, env: 'FishBowl', tempo: float = 120, bpb: int = 4):
        """Basic internal clock

        Args:
            env (FishBowl): Environment for dispatching information
            time (Time): Flow of time
            tempo (float, optional): Beats per minute (tempo). Defaults to 120.
            bpb (int, optional): Number of beats per bar. Defaults to 4.
        """
        self._alive = asyncio.Event()
        self._resumed = asyncio.Event()
        self._resumed.set()
        self._env = env
        self._time = env._time
        self._time_grain = 0.01
        self._tempo = tempo
        self._beats_per_bar = bpb
        self._drift = 0.0

    ## REPR AND STR ############################################################ 

    def __repr__(self) -> str:
        el = self._time._elapsed_time
        return f"{el:1f} -> [{self.tempo}|{self.bar:1f}: {int(self.phase)}/{self._beats_per_bar}] (Drift: {self.drift})"

    #### GETTERS  ############################################################ 

    @property
    def drift(self) -> float:
        return self._drift

    @property
    def beat(self) -> int:
        return self._time._elapsed_time / self.beat_duration

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
        return self._time._elapsed_time % self._beats_per_bar

    @property
    def bpm(self) -> float:
        return self._tempo

    @property
    def tempo(self) -> float:
        return self._tempo

    @property
    def beats_per_bar(self) -> int:
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

    def is_running(self) -> int:
        return self._alive.is_set()

    def is_paused(self) -> int:
        return False if self._resumed.is_set() else True
    
    def start(self):
        """
        Method needed to started ticking the clock without using async 
        syntax and hoops.
        """
        self._alive.set()
        asyncio.create_task(self.run())

    def pause(self):
        """
        Pause the internal clock
        """
        if self._resumed.is_set():
            self._resumed.clear()

    def resume(self):
        if not self._resumed.is_set():
            self._resumed.set()
            
    def stop(self):
        """
        Stop the internal clock
        """
        self._alive.clear()

    async def run(self):
        """Main loop for the internal clock"""
        self._drift = 0.0
        while True:
            await self._resumed.wait()
            if self._alive.is_set():
                begin = perf_counter()
                await asyncio.sleep(self._time_grain - self._drift)
                self._time._elapsed_time += self._time_grain
                self._env.dispatch('tick')
                self._drift = perf_counter() - begin
            else:
                return