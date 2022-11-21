import time

from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import osc_process, osc_send, osc_udp_client

from ..base.handler import BaseHandler
from ..io import read_user_configuration
from ..superdirt.AutoBoot import SuperDirtProcess

__all__ = ("SuperDirtHandler",)


class SuperDirtHandler(BaseHandler):
    def __init__(
        self,
        name: str = "SuperDirt",
        ahead_amount: float = 0.3,
    ):
        super().__init__()
        self._name = name

        # Opening SuperColliderXSuperDirt subprocess
        try:
            config = read_user_configuration()
            self._superdirt_process = SuperDirtProcess(
                startup_file=config.superdirt_config_path,
                verbose=config.verbose_superdirt,
            )
        except OSError as Error:
            print(f"[red]SuperCollider could not be found: {Error}![/red]")

        # Opening a new OSC Client to talk with it
        self._ahead_amount = ahead_amount

        # Setting up environment
        self.env = None
        self._events = {
            "meter": self._superdirt_process.meter,
            "scope": self._superdirt_process.scope,
            "send": self._superdirt_process.send,
            "freqscope": self._superdirt_process.freqscope,
            "dirt_play": self._dirt_play,
            "panic": self._dirt_panic,
            "boot": self._superdirt_process.boot,
            "kill": self._superdirt_process.kill
        }

    def __repr__(self) -> str:
        return f"SuperDirt: {self._name}"

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
        osc_process()

    def __send_timed_message(self, address: str, message: list):
        """Build and send OSC bundles"""
        message = message + [
            "cps",
            (self.env.clock.tempo / 60 / self.env.clock._beats_per_bar),
            "delta",
            1,
        ]
        msg = oscbuildparse.OSCMessage(address, None, message)
        bun = oscbuildparse.OSCBundle(
            oscbuildparse.unixtime2timetag(time.time() + self._ahead_amount),
            [msg],
        )
        osc_send(bun, self._name)
        osc_process()

    def _send(self, address, message):
        self.__send(address=address, message=message)

    def _dirt_play(self, message: list):
        self.__send_timed_message(address="/dirt/play", message=message)

    def _dirt_panic(self):
        self._dirt_play(message=["sound", "superpanic"])

    def send(self, *args, **kwargs):
        """Placeholder"""
        pass
