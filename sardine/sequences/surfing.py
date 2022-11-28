from string import ascii_lowercase, ascii_uppercase
from typing import TYPE_CHECKING, Callable, Union, Optional
from ..base import BaseClock, BaseHandler
from rich.panel import Panel
from rich import print

if TYPE_CHECKING:
    from ..handlers import MidiHandler, OSCHandler, SuperDirtHandler

__all__ = ("Player", "PatternHolder")


class Player:

    """
    A Player is a lone Sender that will be activated by a central surfing
    swimming function. It contains the sender and basic information about
    div, rate, etc...
    """

    def __init__(self, name: str, content: Union[None, dict] = {}):
        self._name = name
        self._content = content

    @classmethod
    def run(cls, func: Callable):
        """
        The run method can be used to schedule any arbitrary function in rhythm just
        like if it was a regular swimming function with a lone function call nested 
        inside it.
        """
        return {"type": "function", "func": func}

    @classmethod
    def play(cls, *args, **kwargs):
        """
        The play method is analog to using the 'D()' send method (SuperDirt).
        """
        return {"type": "sound", "args": args, "kwargs": kwargs}

    @classmethod
    def play_midi(cls, *args, **kwargs):
        """
        The play_midi method is analog to using the 'M()' send method (MIDIOut).
        """
        return {"type": "MIDI", "args": args, "kwargs": kwargs}

    @classmethod
    def play_control(cls, *args, **kwargs):
        """
        The play_control method is analog to using the 'CC()' send method (CCSender).
        """
        return {"type": "MIDI", "args": args, "kwargs": kwargs}

    @classmethod
    def play_osc(cls, *args, **kwargs):
        """
        #TODO: what to do of this?
        """
        return {"type": "OSC", "args": args, "kwargs": kwargs}

    def __rshift__(self, method_result):
        """
        Entry point for allocating a task to a given Player. Possible tasks are 'play',
        'play_midi', 'play_osc', 'play_control' or 'run'. These methods all correspond 
        to one possible simple operation to pattern and more could be added in the 
        future.
        """
        print(Panel.fit(f"[yellow][[red]{self._name}[/red] update!][/yellow]"))
        self._content = method_result

    def __repr__(self) -> str:
        return f"[Player {self._name}]: {self._content}, div: {self._div}, rate: {self._rate}"


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
