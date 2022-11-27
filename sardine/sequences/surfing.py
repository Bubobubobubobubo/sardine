# Surfing mode ###############################################################
#
# Surfing mode is an emulation of the FoxDot (https://foxdot.org/) patterning
# system. It works in a rather similar way, at least for the public interface.
# The rest is just carefully attributing senders to a _global_runner function
# that behaves just like any other swimming function.
#
# It can be useful to quickly lay down some drumming materials while using swim-
# ming functions for more delicate operations :)
################################################################################
from string import ascii_lowercase, ascii_uppercase
from typing import TYPE_CHECKING, Callable, Union, Optional

from rich import print
from rich.panel import Panel

from ..base import BaseClock, BaseHandler

if TYPE_CHECKING:
    from ..handlers import MidiHandler, OSCHandler, SuperDirtHandler

__all__ = ("Player", "PatternHolder")


class Player:

    """
    A Player is a lone Sender that will be activated by a central surfing
    swimming function. It contains the sender and basic information about
    div, rate, etc...
    """

    def __init__(
        self,
        clock,
        name: str,
        content: Union[None, dict] = {},
        rate: Union[int, float] = 1,
    ):
        self._clock = clock
        self._name = name
        self._content = content
        self._rate = rate
        self._dur = 1
        self._div = 1

    @classmethod
    def run(cls, func: Callable):
        """
        The play method will call a SuperDirtSender
        """
        return {"type": "function", "func": func}

    @classmethod
    def play(cls, *args, **kwargs):
        """
        The play method will call a SuperDirtSender
        """
        return {"type": "sound", "args": args, "kwargs": kwargs}

    @classmethod
    def play_midi(cls, *args, **kwargs):
        """
        The play MIDI method will call the Note Send Handler
        """
        return {"type": "MIDI", "args": args, "kwargs": kwargs}

    @classmethod
    def play_osc(cls, *args, **kwargs):
        """
        The play_osc method will call an OSCSender
        """
        return {"type": "OSC", "args": args, "kwargs": kwargs}

    def __rshift__(self, method_result):
        """
        Public method for Players
        """
        print(Panel.fit(f"[yellow][[red]{self._name}[/red] update!][/yellow]"))
        self._content = method_result

    @property
    def rate(self) -> Union[int, float]:
        return self._rate

    @rate.setter
    def rate(self, value: Union[int, float]) -> None:
        self._rate = value

    @property
    def dur(self):
        return self._dur

    @dur.setter
    def dur(self, value: int) -> None:
        pass

    def __repr__(self) -> str:
        return f"[Player {self._name}]: {self._content}, div: {self._div}, rate: {self._rate}"


class PatternHolder(BaseHandler):

    """
    A Pattern Holder, at core, is simply a dict. This dict will contaminate the
    global namespace with references to players, just like FoxDot. Dozens of re-
    ferences to Players() will be inserted in the global namespace to be used by
    musicians.

    Players are senders in disguise. This tiny object will hold all the required
    information to play a sender, including its rate, div, etc...
    """

    def __init__(
        self,
        midi_handler: "MidiHandler",
        osc_handler: "OSCHandler",
        superdirt_handler: "Optional[SuperDirtHandler]",
    ):
        super().__init__()

        self._midisender = midi_handler
        self._oscsender = osc_handler
        self._superdirtsender = superdirt_handler
        self._speed = 1
        self._patterns = {}

    def __repr__(self) -> str:
        return f"<{type(self).__name__} speed={self._speed}>"

    @property
    def again(self):
        return self.env.scheduler.start_func

    @property
    def clock(self) -> BaseClock:
        return self.env.clock

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = float(value)

    def reset(self):
        """
        Reset the internal dictionary of player/senders.
        """
        for key in self._patterns.keys():
            self._patterns[key]._content = {}

    def setup(self):
        """
        Initialisation process. Create the dictionary keys, add one player per
        key. We can't push the dictionary to globals now. It needs to be done
        during the __init__ process like so:

        for (k, v) in self._patterns.items():
            globals()[k] = v
        """
        names = ["P" + l for l in ascii_uppercase + ascii_lowercase]
        self._patterns = {k: Player(clock=self.clock, name=k) for k in names}

    def _global_runner(self, d=1, i=0):
        """
        This is a template for a global swimming function that can hold all
        the player/senders together for scheduling.
        """

        # The delay should be updated dynamically for each loop
        d = self.env.clock.beat_duration / 4
        patterns = [p for p in self._patterns.values() if p._content not in [None, {}]]

        for player in patterns:
            #TODO: rewrite surfing mode function
            try:
                pass
            except Exception as e:
                continue
        self.again(self._global_runner, d=d, i=i + 1)
