from ..Components.BaseClock import BaseClock
from typing import TYPE_CHECKING
from time import perf_counter
import asyncio

if TYPE_CHECKING:
    from .FishBowl import FishBowl
    from .Time import Time

class Clock(BaseClock):

    def __init__(self, env: 'FishBowl', time: 'Time', tempo: float = 120, bpb: int = 4):
        """Basic internal clock

        Args:
            env (FishBowl): Environment for dispatching information
            time (Time): Flow of time
            tempo (float, optional): Beats per minute (tempo). Defaults to 120.
            bpb (int, optional): Number of beats per bar. Defaults to 4.
        """
        self._env = env
        self._time = time
        self._time_grain = 0.01
        self._tempo = tempo
        self._beats_per_bar = bpb
        self._accel = 0.0

    ## REPR AND STR ############################################################ 

    def __repr__(self) -> str:
        el = self._time._elapsed_time
        return f"{el:1f} -> [{self.tempo}|{self.bar:1f}: {int(self.phase)}/{self._beats_per_bar}]"


    #### GETTERS  ############################################################ 

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
    def accel(self) -> float:
        return self._accel

    @property
    def beats_per_bar(self) -> int:
        return self._beats_per_bar

    #### SETTERS ############################################################ 

    @accel.setter
    def accel(self, value: int):
        """
        Accel stands for acceleration. In active MIDI mode, accel acts as a way
        to nudge the clock to run faster or slower (from 0 to 100%). It can be
        quite useful when dealing with a musician that can't really use any
        synchronisation protocol. Beware, you will have to manually reset the
        accel amount after setting it if you want to stop and not fasten the
        clock.

        Args:
            value (int): a nudge factor from 0 to 100%

        Raises:
            ValueError: if 'value' exceeds 100%
        """
        if value >= 100:
            raise ValueError("Cannot set acceleration above 100%.")
        self._accel = value

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

    ## MAIN LOOP  ############################################################## 
    
    def start(self):
        """
        Method needed to started ticking the clock without using async 
        syntax and hoops.
        """
        asyncio.create_task(self.run())

    async def run(self):
        """Main loop for the internal clock"""
        drift = 0.0
        while True:
            begin = perf_counter()
            await asyncio.sleep(self._time_grain - drift)
            self._time._elapsed_time += self._time_grain
            self._env.dispatch('tick')
            drift = perf_counter() - begin