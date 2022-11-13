#!/usr/bin/env python3
import asyncio
from typing import Callable, Any
from time import time
from typing import Union, TYPE_CHECKING, List
from osc4py3 import oscbuildparse
from functools import partial
from osc4py3.as_eventloop import (
    osc_startup,
    osc_udp_client,
    osc_udp_server,
    osc_method,
    osc_send,
    osc_process,
    osc_terminate,
)
from osc4py3.oscmethod import *  # does OSCARG_XXX
from rich import print

if TYPE_CHECKING:
    from ..clock import Clock

__all__ = ("Receiver", "Client", "client", "dirt")


def flatten(l):
    if isinstance(l, (list, tuple)):
        if len(l) > 1:
            return [l[0]] + flatten(l[1:])
        else:
            return l[0]
    else:
        return [l]


class Receiver:

    """
    Incomplete and temporary implementation of an OSC message receiver.
    Will be completed later on when I will have found the best method to
    log incoming values.
    """

    def __init__(
        self, port: int, ip: str = "127.0.0.1", name: str = "receiver", at: int = 0
    ):
        """
        Keyword parameters
        ip: str -- IP address
        port: int -- network port
        name: str -- Name attributed to the OSC receiver
        """
        self._ip, self._port, self._name = ip, port, name
        self._server = osc_udp_server(ip, port, name)
        self._watched_values = {}

    def _generic_store(self, address) -> None:
        """Generic storage function to attach to a given address"""

        def generic_value_tracker(*args, **kwargs):
            """Generic value tracker to be attached to an address"""
            self._watched_values[address] = {"args": flatten(args), "kwargs": kwargs}
            return (args, kwargs)

        osc_method(address, generic_value_tracker, argscheme=OSCARG_DATA)

    def watch(self, address: str):
        """
        Watch the value of a given OSC address. Will be recorded in memory
        in the self._watched_values dictionary accessible through the get()
        method
        """
        print(f"[yellow]Watching address [red]{address}[/red].[/yellow]")
        self._generic_store(address)

    def attach(self, address: str, function: Callable, watch: bool = False):
        """
        Attach a callback to a given address. You can also toggle the watch
        boolean value to tell if the value should be tracked by the receiver.
        It allows returning values from the callback to be retrieved later in
        through the get(address) method.
        """
        print(
            f"[yellow]Attaching function [red]{function.__name__}[/red] to address [red]{address}[/red][/yellow]"
        )
        osc_method(address, function)
        if watch:
            self.watch(address)

    def get(self, address: str) -> Union[Any, None]:
        """Get a watched value. Return None if not found"""
        try:
            return self._watched_values[address]
        except KeyError:
            return None


class Client:
    def __init__(
        self,
        ip: str = "127.0.0.1",
        port: int = 57120,
        name: str = "SuperDirt",
        ahead_amount: Union[float, int] = 0.03,
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

    def _get_clock_information(self, clock: "Clock") -> list:
        """Send out everything you can possibly send about the clock"""
        return (
            ["/cps", (clock.bpm / 60 / clock.beat_per_bar)],
            ["/bpm", clock.bpm],
            ["/beat", clock.beat],
            ["/bar", clock.bar],
            ["/tick", clock.tick],
            ["/phase", clock.phase],
            ["/accel", clock.accel],
        )

    def _send_clock_information(self, clock: "Clock"):
        for element in self._get_clock_information(clock):
            self._send(clock=clock, address=element[0], message=[element[1]])

    def _send(self, clock: "Clock", address: str, message):
        """Build user-made OSC messages"""
        msg = oscbuildparse.OSCMessage(address, None, message)
        bun = oscbuildparse.OSCBundle(
            oscbuildparse.unixtime2timetag(time() + self._ahead_amount), [msg]
        )
        osc_send(bun, self._name)
        osc_process()

    def send_timed_message(self, message, clock):
        """Build and send OSC bundles"""
        message = message + [
            "cps",
            (clock.bpm / 60 / clock.beat_per_bar),
            "delta",
            (clock._get_tick_duration() * 100),
        ]
        msg = oscbuildparse.OSCMessage("/dirt/play", None, message)
        bun = oscbuildparse.OSCBundle(
            oscbuildparse.unixtime2timetag(time() + self._ahead_amount), [msg]
        )
        osc_send(bun, self._name)
        osc_process()

    def kill(self):
        """Terminate OSC connexion"""
        osc_terminate()


client = Client()


def dirt(message, clock, ahead_amount: Union[int, float] = 0.03):
    """Sending messages to SuperDirt/SuperCollider"""
    client.ahead_amount = ahead_amount
    client.send_timed_message(message=message, clock=clock)
