from typing import Union
from dataclasses import dataclass
from enum import Enum, auto

__all__ = ("Player",)

NUMBER = Union[float, int]

class PlayerType(Enum):
    INACTIVE    = auto()
    FUNCTION    = auto()
    SUPERDIRT   = auto()
    MIDINOTE    = auto()
    MIDICONTROL = auto()
    OSC         = auto()

@dataclass
class PlayerInformation:
    player_type: str
    message: dict
    iterator: int
    divisor: int
    rate: NUMBER
    iteration_count: int

class Player:

    """
    A Player is a lone Sender that will be activated by a central surfing
    swimming function. It contains the sender and basic information about
    div, rate, etc...
    """

    def __init__(self, 
                 name: str, 
                 info: PlayerInformation,
    ):
        self._name = name
        self._info = info
