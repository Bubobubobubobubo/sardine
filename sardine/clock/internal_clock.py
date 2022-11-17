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
        self._type = "InternalClock"

        # Time related attributes
        self.beat_duration: float = 0.0
        self.tempo = tempo
        self.beats_per_bar = bpb

    ## REPR AND STR ############################################################

    def __repr__(self) -> str:
        return (
            "({0._type} {0.time:1f}) -> [{0.tempo}|{0.bar:1f}: "
            "{0.phase}/{0.beats_per_bar}]"
        ).format(self)

    #### GETTERS  ############################################################

    @property
    def internal_time(self) -> float:
        return time.monotonic()

    @property
    def bar(self) -> int:
        return self.beat // self.beats_per_bar

    @property
    def beat(self) -> int:
        return self.time // self.beat_duration

    @property
    def phase(self) -> float:
        return self.time % self.beat_duration

    @property
    def tempo(self) -> int:
        return self._tempo

    #### SETTERS ############################################################

    @tempo.setter
    def tempo(self, new_tempo: int):
        if not 1 <= new_tempo <= 999:
            raise ValueError("new tempo must be within 1 and 999")

        self._tempo = new_tempo
        self.beat_duration = 60 / new_tempo

    ## METHODS  ##############################################################

    async def run(self):
        # The internal clock simply uses the system's time
        # so we don't need to do any polling loop here
        self.internal_origin = self.internal_time
        await asyncio.sleep(math.inf)
