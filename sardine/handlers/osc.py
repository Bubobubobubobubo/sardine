import time
from itertools import chain
from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import *
from osc4py3.oscmethod import *
from ..base.handler import BaseHandler
from ..sequences import Chord
from .osc_loop import OSCLoop
from .sender import (
        VALUES,
        Sender, 
        _alias_param,
)

__all__ = ("OSCHandler",)

class OSCHandler(BaseHandler, Sender):
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
        loop.add_child(self)

        # Setting up OSC Connexion
        self._ip, self._port, self._name = (ip, port, name)
        self._ahead_amount = ahead_amount
        self.client = osc_udp_client(
                address=self._ip, 
                port=self._port, 
                name=self._name
        )
        self._events = {"send": self._send}

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self._name} ip={self._ip} port={self._port}>"

    def setup(self):
        for event in self._events:
            self.env.register_hook(event, self)

    def hook(self, event: str, *args):
        func = self._events[event]
        func(*args)

    def _send(self, address: str, message: list) -> None:
        msg = oscbuildparse.OSCMessage(address, None, message)
        bun = oscbuildparse.OSCBundle(
            oscbuildparse.unixtime2timetag(time.time() + self._ahead_amount),
            [msg],
        )
        osc_send(bun, self._name)

    @_alias_param(name="iterator", alias="i")
    @_alias_param(name="divisor", alias="d")
    @_alias_param(name="rate", alias="r")
    def send(
        self,
        address: VALUES = 60,
        iterator: int = 0,
        divisor: int = 1,
        rate: float = 1,
        **kwargs,
    ) -> None:

        if iterator % divisor != 0:
            return

        pattern = kwargs
        pattern["address"] = address

        pattern = self.pattern_reduce(
            pattern=pattern, iterator=iterator, divisor=divisor, rate=rate
        )

        is_polyphonic = any(isinstance(v, Chord) for v in pattern.values())

        if is_polyphonic:
            for message in self.reduce_polyphonic_message(pattern):
                if not isinstance(message["address"], type(None)):
                    # Removing the address key from the final list
                    del message["address"]
                    final_message = list(chain(*sorted(message.items())))
                    self._send(address="/" + message["address"], message=final_message)
        else:
            address = pattern["address"]
            if not isinstance(pattern["address"], type(None)):
                # Removing the address key from the final list
                del pattern["address"]
                final_message = list(chain(*sorted(pattern.items())))
                self._send(address="/" + address, message=final_message)
