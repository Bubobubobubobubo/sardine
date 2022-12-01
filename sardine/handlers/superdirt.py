import time
from itertools import chain

from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import osc_send, osc_udp_client

from ..io import read_user_configuration
from ..superdirt.AutoBoot import SuperDirtProcess
from .sender import Number, NumericElement, ParsableElement, Sender, _alias_param

__all__ = ("SuperDirtHandler",)


class SuperDirtHandler(Sender):
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
        self._osc_client = osc_udp_client(
            address="127.0.0.1", port=57120, name=self._name
        )
        self._ahead_amount = ahead_amount

        # Setting up environment
        self._events = {
            "meter": self._superdirt_process.meter,
            "scope": self._superdirt_process.scope,
            "trace": self._superdirt_process.trace(True),
            "untrace": self._superdirt_process.trace(False),
            "send": self._superdirt_process.send,
            "freqscope": self._superdirt_process.freqscope,
            "dirt_play": self._dirt_play,
            "panic": self._dirt_panic,
            "boot": self._superdirt_process.boot,
            "kill": self._superdirt_process.kill,
        }

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

    @_alias_param(name="iterator", alias="i")
    @_alias_param(name="divisor", alias="d")
    @_alias_param(name="rate", alias="r")
    def send(
        self,
        sound: str,
        orbit: NumericElement = 0,
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        **pattern: ParsableElement,
    ):

        if iterator % divisor != 0:
            return

        pattern["sound"] = sound
        pattern["orbit"] = 0
        pattern["cps"] = round(self.env.clock.phase, 4)
        pattern["cycle"] = (
            self.env.clock.bar * self.env.clock.beats_per_bar
        ) + self.env.clock.beat

        for message in self.pattern_reduce(pattern, iterator, divisor, rate):
            serialized = list(chain(*sorted(message.items())))
            self._dirt_play(serialized)
