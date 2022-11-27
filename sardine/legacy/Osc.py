#!/usr/bin/env python3

from osc4py3.oscmethod import *  # does OSCARG_XXX
from rich import print
from typing import TYPE_CHECKING, Any, Callable, Union
from osc4py3.as_eventloop import (
    osc_method,
    osc_udp_server,
)

__all__ = ("Receiver", )


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
