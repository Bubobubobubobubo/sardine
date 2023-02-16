import time
from itertools import chain
from typing import Optional, List

from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import osc_send, osc_udp_client

from ..utils import alias_param
from .osc_loop import OSCLoop
from .sender import Number, NumericElement, ParsableElement, Sender, StringElement

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

        loop.add_child(self, setup=True)

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

    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    def send(
        self,
        sound: Optional[StringElement|List[StringElement]],
        orbit: NumericElement = 0,
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        **pattern: ParsableElement,
    ):

        if sound is None:
            return


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
