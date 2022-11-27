from typing import Any, Callable, Optional, Union

from osc4py3.as_eventloop import *
from osc4py3.oscchannel import TransportChannel, get_channel
from osc4py3.oscmethod import *
from rich import print

from ..base.handler import BaseHandler
from .osc_loop import OSCLoop

__all__ = ("OSCInHandler",)


def flatten(l):
    if isinstance(l, (list, tuple)):
        if len(l) > 1:
            return [l[0]] + flatten(l[1:])
        else:
            return l[0]
    else:
        return [l]


class OSCInHandler(BaseHandler):
    def __init__(
        self,
        loop: OSCLoop,
        ip: str = "127.0.0.1",
        port: int = 11223,
        name: str = "OSCIn",
    ):
        super().__init__()
        self.loop = loop
        loop.add_child(self)

        self._ip, self._port, self._name = ip, port, name
        self._watched_values = {}

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self._name} ip={self._ip} port={self._port}>"

    # Handler methods

    def setup(self):
        osc_udp_server(self._ip, self._port, self._name)

    def teardown(self):
        channel: Optional[TransportChannel] = get_channel(self._name)
        if channel is not None:
            channel.terminate()

    def hook(self, event: str, *args): ...

    # Interface

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

    def remote(self, address: str):
        """
        Remote for controlling Sardine from an external client by talking directly to
        the fish_bowl dispatch system. If the address matches an internal function de-
        clared by some handler, the dispatch function will be called and *args will be
        forwarded as well.

        address: address matching to a dispatch function (like 'pause', 'stop', etc..)
        """
        print("Attaching address to matching incoming message")

        def event_dispatcher(address, *args) -> None:
            print(f"Event Name: {address}")
            self.env.dispatch(address, *args)

        osc_method(address, event_dispatcher, argscheme=OSCARG_DATA)

    def get(self, address: str) -> Union[Any, None]:
        """Get a watched value. Return None if not found"""
        try:
            return self._watched_values[address]
        except KeyError:
            return None
