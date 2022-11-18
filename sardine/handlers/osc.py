import time

from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import osc_process, osc_send, osc_udp_client
from osc4py3.oscmethod import *

from ..base.handler import BaseHandler

__all__ = ("OSCHandler",)


class OSCHandler(BaseHandler):
    def __init__(
        self,
        ip: str = "127.0.0.1",
        port: int = 23456,
        name: str = "OSCSender",
        ahead_amount: float = 0.0,
    ):
        super().__init__()

        # Setting up OSC Connexion
        self._ip, self._port, self._name = (ip, port, name)
        self._ahead_amount = ahead_amount
        osc_process()
        self.client = osc_udp_client(
            address=self._ip, port=self._port, name=self._name
        )

        self._events = {"send": self._send}

    def __repr__(self) -> str:
        return f"OSC {self._name}: {self._ip}:{self._port}"

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
        osc_process()
