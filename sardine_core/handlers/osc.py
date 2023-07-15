import time
from itertools import chain
from typing import Optional

from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import *
from osc4py3.oscmethod import *

from ..utils import alias_param
from .osc_loop import OSCLoop
from .sender import Number, NumericElement, Sender, StringElement

__all__ = ("OSCHandler",)


class OSCHandler(Sender):
    def __init__(
        self,
        loop: OSCLoop,
        ip: str = "127.0.0.1",
        port: int = 23456,
        name: str = "OSCSender",
        ahead_amount: float = 0.0,
    ):
        super().__init__()
        self.loop = loop

        # Setting up OSC Connexion
        self._ip, self._port, self._name = (ip, port, name)
        self._ahead_amount = ahead_amount
        self.client = osc_udp_client(address=self._ip, port=self._port, name=self._name)
        self._events = {"send": self._send}
        self._defaults: dict = {}

        loop.add_child(self, setup=True)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self._name} ip={self._ip!r} port={self._port}>"

    def setup(self):
        for event in self._events:
            self.env.register_hook(event, self)

    def hook(self, event: str, *args):
        func = self._events[event]
        func(*args)

    # Global parameters
    @property
    def defaults(self):
        return self._defaults

    def _send(self, address: str, message: list) -> None:
        msg = oscbuildparse.OSCMessage(address, None, message)
        bun = oscbuildparse.OSCBundle(
            oscbuildparse.unixtime2timetag(time.time() + self._ahead_amount),
            [msg],
        )
        osc_send(bun, self._name)

    def send_raw(self, address: str, message: list) -> None:
        """
        Public alias for the _send function. It can sometimes be useful to have it
        when we do want to write some raw OSC message without formatting it in the
        expected SuperDirt format.
        """
        self._send(address, message)

    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    @alias_param(name="sorted", alias="s")
    def send(
        self,
        address: Optional[StringElement],
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        sort: bool = True,
        **pattern: NumericElement,
    ) -> None:
        if address is None:
            return

        if self.apply_conditional_mask_to_bars(
            pattern=pattern,
        ):
            return

        pattern["address"] = address
        deadline = self.env.clock.shifted_time
        for message in self.pattern_reduce(pattern, iterator, divisor, rate):
            if message["address"] is None:
                continue
            address = message.pop("address")
            if sort:
                serialized = list(chain(*sorted(message.items())))
            else:
                serialized = list(chain(*message.items()))
            self.call_timed(deadline, self._send, f"/{address}", serialized)
