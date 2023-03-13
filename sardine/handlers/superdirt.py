import time
from itertools import chain
from typing import Optional, List

from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import osc_send, osc_udp_client

from ..utils import alias_param
from .osc_loop import OSCLoop
from .sender import (
    Number,
    NumericElement,
    ParsableElement,
    Sender,
    StringElement
)

__all__ = ("SuperDirtHandler",)


class SuperDirtHandler(Sender):
    def __init__(
        self,
        *,
        loop: OSCLoop,
        name: str = "SuperDirt",
        ahead_amount: float = 0.3,
    ):
        super().__init__()
        self._name = name
        self.loop = loop

        # Opening a new OSC Client to talk with it
        self._osc_client = osc_udp_client(
            address="127.0.0.1", port=57120, name=self._name
        )
        self._ahead_amount = ahead_amount

        # Setting up environment
        self._events = {
            "dirt_play": self._dirt_play,
            "panic": self._dirt_panic,
        }

        self._ziffers_parser = None

        loop.add_child(self, setup=True)

    # Ziffers implementation
    @property
    def ziffers_parser(self):
        return self._ziffers_parser

    @ziffers_parser.setter
    def ziffers_parser(self, parser):
        self._ziffers_parser = parser

    @property
    def nudge(self):
        return self._ahead_amount

    @nudge.setter
    def nudge(self, amount: int | float):
        self._ahead_amount = amount

    def __repr__(self) -> str:
        return f"<SuperDirt: {self._name} nudge: {self._ahead_amount}>"

    def setup(self):
        for event in self._events:
            self.register(event)

    def hook(self, event: str, *args):
        func = self._events[event]
        func(*args)

    def __send(self, address: str, message: list) -> None:
        msg = oscbuildparse.OSCMessage(address, None, message)
        bun = oscbuildparse.OSCBundle(
            oscbuildparse.unixtime2timetag(time.time() + self._ahead_amount),
            [msg],
        )
        osc_send(bun, self._name)

    def __send_timed_message(self, address: str, message: list):
        """Build and send OSC bundles"""
        msg = oscbuildparse.OSCMessage(address, None, message)
        bun = oscbuildparse.OSCBundle(
            oscbuildparse.unixtime2timetag(time.time() + self._ahead_amount),
            [msg],
        )
        osc_send(bun, self._name)

    def _send(self, address, message):
        self.__send(address=address, message=message)

    def _dirt_play(self, message: list):
        self.__send_timed_message(address="/dirt/play", message=message)

    def _dirt_panic(self):
        self._dirt_play(message=["sound", "superpanic"])

    def _parse_aliases(self, pattern: dict):
        """Parse aliases for certain keys in the pattern (lpf -> cutoff)"""

        def rename_keys(initial_dictionary: dict, aliases: dict) -> dict:
            return dict([(aliases.get(k, k), v) for k, v in initial_dictionary.items()])

        aliases = {
            "lpf": "cutoff",
            "lpq": "resonance",
            "hpf": "hcutoff",
            "lpq": "resonance",
            "bpf": "bandf",
            "bpq": "resonance",
            "res": "resonance",
            "midi": "midinote",
            "n": "midinote",
            "oct": "octave",
            "accel": "accelerate",
            "leg": "legato",
            "delayt": "delaytime",
            "delayfb": "delayfeedback",
            "phasr": "phaserrate",
            "phasd": "phaserdepth",
            "tremrate": "tremolorate",
            "tremd": "tremolodepth",
            "dist": "distort",
        }
        return rename_keys(pattern, aliases)


    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    def send(
        self,
        sound: Optional[StringElement | List[StringElement]],
        orbit: NumericElement = 0,
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        **pattern: ParsableElement,
    ):
        if sound is None:
            return
    
        # If the result of this cycle computation is false, we don't have to play at all
        if not self.cycle_should_play(
                pattern.get("struct", None),
                pattern.get("on", None)):
            return

        # Replace some shortcut parameters by their real name
        pattern = self._parse_aliases(pattern)

        pattern["sound"] = sound
        pattern["orbit"] = orbit
        pattern["cps"] = round(self.env.clock.phase, 4)
        pattern["cycle"] = (
            self.env.clock.bar * self.env.clock.beats_per_bar
        ) + self.env.clock.beat

        deadline = self.env.clock.shifted_time
        for message in self.pattern_reduce(pattern, iterator, divisor, rate):
            if message["sound"] is None:
                continue
            serialized = list(chain(*sorted(message.items())))
            self.call_timed(deadline, self._dirt_play, serialized)

    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    def send_ziffers(
        self,
        sound: Optional[StringElement | List[StringElement]],
        ziff: str,
        orbit: NumericElement = 0,
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        key: str = "C4",
        scale: str = "IONIAN",
        **pattern: ParsableElement,
    ) -> int | float:
        # Replace some shortcut parameters by their real name
        pattern = self._parse_aliases(pattern)

        # If the result of this cycle computation is false, we don't have to play at all
        if not self.cycle_should_play(
                pattern.get("struct", None),
                pattern.get("on", None)):
            return

        if not self._ziffers_parser:
            raise Exception("The ziffers package is not imported!")
        else:
            ziffer = self._ziffers_parser(ziff, scale=scale, key=key)[iterator]
            try:
                freq = ziffer.freq
            except AttributeError:  # if there is no note, it must be a silence
                try:
                    freq = []
                    for pitch in ziffer.pitch_classes:
                        freq.append(pitch.freq)
                except AttributeError:
                    if ziffer.text == "r":
                        sound = "rest"
                    else:
                        sound = None  # the ziffers pattern takes precedence
                    freq = 0

            if isinstance(freq, list):
                freq = f"{{{', '.join([str(x) for x in freq])}}}"

        if sound is None:
            return

        if sound != "rest":
            pattern["freq"] = freq
            pattern["sound"] = sound
            pattern["orbit"] = orbit
            pattern["cps"] = round(self.env.clock.phase, 4)
            pattern["cycle"] = (
                self.env.clock.bar * self.env.clock.beats_per_bar
            ) + self.env.clock.beat

            deadline = self.env.clock.shifted_time
            for message in self.pattern_reduce(pattern, iterator, divisor, rate):
                if message["sound"] is None:
                    continue
                serialized = list(chain(*sorted(message.items())))
                self.call_timed(deadline, self._dirt_play, serialized)

        try:
            if isinstance(ziffer.duration, (int, float)):
                return ziffer.duration * (self.env.clock.beats_per_bar)
            elif isinstance(ziffer.duration, (list)):
                return ziffer.duration[0] * (self.env.clock.beats_per_bar)
        except AttributeError:
            return 1.0 * (self.env.clock.beats_per_bar)
