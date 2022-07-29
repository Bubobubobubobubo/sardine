from typing import Union
from math import floor

class Time:
    def __init__(self, ppqn: int, bar: Union[int, float] = 0,
                 beat: Union[int, float] = 0, phase: int = 0):

        """
        OBSOLETE // DO NOT USE THIS CLASS

        Generate a time target in the future. The function needs
        a PPQN to be used as reference. The PPQN will be used to
        decompose bars and beats in a given nb of PPQN to reach the
        target.

        ppqn: int -- How many PPQN are used by the system
        bar:  Union[int, float]  -- How many bars in the future
        beat: Union[int, float]  -- How many beats in the future
        phase: Union[int, float] -- How many PPQN in the future
        """

        self.ppqn = ppqn
        bar_standard, beat_standard = ppqn * 4, ppqn
        self.bar = floor(bar_standard * bar)
        self.beat = floor(beat_standard * beat)
        self.phase = phase

    def target(self) -> int:
        """ Return the number of PPQN to reach target """
        return self.beat + self.bar + self.phase



