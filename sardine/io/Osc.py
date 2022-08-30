#!/usr/bin/env python3
import asyncio
from time import time
from typing import Union, TYPE_CHECKING, List
from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import (
    osc_startup,
    osc_udp_client,
    osc_send,
    osc_process,
    osc_terminate,
)

if TYPE_CHECKING:
    from ..clock import Clock

__all__ = ("Client", "client", "dirt")


class Client:
    def __init__(
        self,
        ip: str = "127.0.0.1",
        port: int = 57120,
        name: str = "SuperDirt",
        ahead_amount: Union[float, int] = 0.5,
        at: int = 0,
    ):

        """
        Keyword parameters
        ip: str -- IP
        port: int -- network port
        name: str -- Name attributed to the OSC connexion
        ahead_amount: Union[float, int] -- (in ms.) send timestamp
                      in the future, x ms. after current time.
        """

        self._ip, self._port = (ip, port)
        self._name, self._ahead_amount = (name, ahead_amount)
        self.after: int = at
        osc_startup()
        self.client = osc_udp_client(address=self._ip, port=self._port, name=self._name)

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value

    @property
    def ahead_amount(self):
        return self._ahead_amount

    @ahead_amount.setter
    def ahead_amount(self, value):
        self._ahead_amount = value

    def send(
        self, clock: "Clock", address: str, message: oscbuildparse.OSCBundle
    ) -> None:
        async def _waiter():
            await handle
            self._send(clock, address, message)

        ticks = clock.get_beat_ticks(self.after, sync=False)
        handle = clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name="osc-scheduler")

    def _get_clock_information(clock: "Clock") -> list:
        """Send out everything you can possibly send about the clock"""
        return  [["/cps", (clock.bpm / 60 / 4)],
                ["/s_beat", clock.beat],
                ["/s_bar", clock.bar],
                ["/s_tick", clock.tick],
                ["/s_phase", clock.phase],
                ["/s_accel", clock.accel]]

    def _send(self, clock: "Clock", address: str, message):
        """Build user-made OSC messages"""
        msg = oscbuildparse.OSCMessage(address, None, message)
        bun = oscbuildparse.OSCBundle(
            oscbuildparse.unixtime2timetag(time() + self._ahead_amount), [msg]
        )
        osc_send(bun, self._name)
        osc_process()

    def send_timed_message(self, message):
        """Build and send OSC bundles"""
        msg = oscbuildparse.OSCMessage("/play2", None, message)
        bun = oscbuildparse.OSCBundle(
            oscbuildparse.unixtime2timetag(time() + self._ahead_amount), [msg]
        )
        osc_send(bun, self._name)
        osc_process()

    def kill(self):
        """Terminate OSC connexion"""
        osc_terminate()


client = Client()


def dirt(message):
    """Sending messages to SuperDirt/SuperCollider"""
    client.send_timed_message(message)
