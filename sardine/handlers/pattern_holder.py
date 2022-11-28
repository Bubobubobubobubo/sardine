from string import ascii_lowercase, ascii_uppercase
from typing import (
        TYPE_CHECKING, 
        Optional
)
from ..base import BaseHandler, BaseClock
from ..surfing import Player

if TYPE_CHECKING:
    from ..handlers import (
            MidiHandler,
            OSCHandler, 
            SuperDirtHandler
    )

__all__ = ('PatternHolder',)

class PatternHolder(BaseHandler):

    """
    A Pattern Holder, at core, is simply a dict. This dict will contaminate the global
    namespace with references to players, just like FoxDot. Dozens of re ferences to
    Players() will be inserted in the global namespace to be used by musicians.

    Players are swimming functions in disguise, with a better and terser syntax. Howe-
    ver, you loose the ability of having multiple statements per swimming function. Each
    Player can have its own rate, it's own patterned rhythm, etc... It should behave just
    like a regular swimming function.
    """

    def __init__(
        self,
        clock,
        midi_handler: "MidiHandler",
        osc_handler: "OSCHandler",
        superdirt_handler: "Optional[SuperDirtHandler]",
    ):
        super().__init__()

        self._clock = clock
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

    def _template_runner(self):
        """
        Template runner that every Player will eventually specialise with its own 
        data. 
        """
        ...

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
