# QuickStep mode ###############################################################
#
# Quickstep is another dance similar to FoxTrot. All in all, this is as bad pun
# to name this feature: an emulation of FoxDot (https://foxdot.org/) patterning
# system. It works in a rather similar way, at least for the public interface.
# The rest is just carefully attributing senders to a _global_runner function
# that behaves just like any other swimming function.
#
# It can be useful to quickly lay down some drumming materials while using swim-
# ming functions for more delicate operations :)
################################################################################
from string import ascii_uppercase, ascii_lowercase
from typing import Union, TYPE_CHECKING
from rich import print
from rich.panel import Panel


if TYPE_CHECKING:
    from ..io.MIDISender import MIDISender
    from ..io.SuperDirtSender import SuperDirtSender
    from ..io.OSCSender import OSCSender

__all__ = ("Player", "PatternHolder")


class Player:

    """
    A Player is a lone Sender that will be activated by a central QuickStep
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
        self._div = int(
            self._conversion_function(low=1, high=self._clock.ppqn * 8, value=self._dur)
        )

    def _conversion_function(
        self, low: Union[int, float], high: Union[int, float], value: Union[int, float]
    ) -> int:
        """Internal function performing the conversion"""

        def remap(x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

        return remap(value, 0, 4, 1, 127)

    @classmethod
    def play(cls, *args, **kwargs):
        """
        The play method will call a SuperDirtSender
        """
        return {"type": "sound", "args": args, "kwargs": kwargs}

    @classmethod
    def play_midi(cls, *args, **kwargs):
        """
        The play MIDI method will call a MIDISender
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
        """
        Div for surfboards does not have the same behavior it has in regular swimming
        functions. It would be counter-intuitive. In that mode, the div should be in-
        terpreted as a speed, with speed=0.01 being the absolute lowest speed a surf-
        board can go. It means that the lowest value is some arbitrary cap we choose
        to follow such as self._clock.ppqn * 4 for instance.

        The high limit should feel like we are going insanely fast but still yield to
        something like div=1 internally.

        Args:
            value (int): the new 'speed' factor
        """
        slow_limit = self._clock.ppqn * 8
        fast_limit = 1

        new_div = int(self._conversion_function(slow_limit, fast_limit, value))
        # Dumb corrections
        new_div = 1 if new_div == 0 else new_div
        new_div = slow_limit if new_div > slow_limit else new_div

        self._dur = value
        self._div = new_div

    def __repr__(self) -> str:
        return f"[Player {self._name}]: {self._content}, div: {self._div}, rate: {self._rate}"


class PatternHolder:

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
        MIDISender: "MIDISender",
        OSCSender: "OSCSender",
        SuperDirtSender: "SuperDirtSender",
        clock,
    ):
        self._midisender = MIDISender
        self._oscsender = OSCSender
        self._superdirtsender = SuperDirtSender
        self._clock = clock
        self._speed = 1
        self._patterns = {}
        self._init_internal_dictionary()

    def __repr__(self) -> str:
        return f"Surfboard || speed: {self._speed}"

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

    def _init_internal_dictionary(self):
        """
        Initialisation process. Create the dictionary keys, add one player per
        key. We can't push the dictionary to globals now. It needs to be done
        during the __init__ process like so:

        for (k, v) in self._patterns.items():
            globals()[k] = v
        """
        names = ["P" + l for l in ascii_uppercase + ascii_lowercase]
        self._patterns = {k: Player(clock=self._clock, name=k) for k in names}

    def _global_runner(self, d=1, i=0):
        """
        This is a template for a global swimming function that can hold all
        the player/senders together for scheduling.
        """
        d = self._speed / (self._clock.ppqn / 2)
        patterns = [p for p in self._patterns.values() if p._content not in [None, {}]]
        for player in patterns:
            try:
                if player._content["type"] == "MIDI":
                    self._midisender(
                        note=player._content["args"][0], **player._content["kwargs"]
                    ).out(i=i, div=player._div, rate=player._rate)
                elif player._content["type"] == "OSC":
                    self._oscsender(
                        *player._content["args"], **player._content["kwargs"]
                    ).out(i=i, div=player._div, rate=player._rate)
                elif player._content["type"] == "sound":
                    self._superdirtsender(
                        *player._content["args"], **player._content["kwargs"]
                    ).out(i=i, div=player._div, rate=player._rate)
            except Exception as e:
                continue
        self._clock.schedule_func(self._global_runner, d=d, i=i + 1)
