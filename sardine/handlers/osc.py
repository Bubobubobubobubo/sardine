import time
from functools import wraps
from itertools import chain
from math import floor
from typing import Union

from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import *
from osc4py3.oscmethod import *

from ..base.handler import BaseHandler
from ..sequences import Chord
from .osc_loop import OSCLoop

__all__ = ("OSCHandler",)

VALUES = Union[int, float, list, str]
PATTERN = dict[str, list[float | int | list | str]]
REDUCED_PATTERN = dict[str, list[float | int]]


class OSCHandler(BaseHandler):
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

    def pattern_element(self, div: int, rate: int, iterator: int, pattern: list) -> int:
        """Joseph Enguehard's algorithm for solving iteration speed"""
        return floor(iterator * rate / div) % len(pattern)

    def pattern_reduce(
        self,
        pattern: PATTERN,
        iterator: int,
        divisor: int,
        rate: float,
    ) -> dict:
        pattern = {
            k: self.env.parser.parse(v) if isinstance(v, str) else v
            for k, v in pattern.items()
        }
        pattern = {
            k: v[
                self.pattern_element(
                    div=divisor, rate=rate, iterator=iterator, pattern=v
                )
            ]
            if hasattr(v, "__getitem__")
            else v
            for k, v in pattern.items()
        }
        return pattern

    def reduce_polyphonic_message(self, pattern: PATTERN) -> list[dict]:
        """
        Reduce a polyphonic message to a list of messages represented as
        dictionaries holding values to be sent through the MIDI Port
        """
        message_list: list = []
        length = [
            x for x in filter(lambda x: hasattr(x, "__getitem__"), pattern.values())
        ]
        length = max([len(i) for i in length])

        # Break the chords into lists
        pattern = {
            k: list(value) if isinstance(value, Chord) else value
            for k, value in pattern.items()
        }

        for _ in range(length):
            message_list.append(
                {
                    k: v[_ % len(v)] if isinstance(v, (Chord, list)) else v
                    for k, v in pattern.items()
                }
            )
        return message_list

    @staticmethod
    def _alias_param(name, alias):
        """Alias a keyword parameter in a function. Throws a TypeError when a value is
        given for both the original kwarg and the alias.
        """
        MISSING = object()

        def deco(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                alias_value = kwargs.pop(alias, MISSING)
                if alias_value is not MISSING:
                    if name in kwargs:
                        raise TypeError(
                            f"Cannot pass both {name!r} and {alias!r} in call"
                        )
                    kwargs[name] = alias_value
                return func(*args, **kwargs)

            return wrapper

        return deco

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
