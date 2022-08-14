#!/usr/bin/env python3
import asyncio
import pprint
import functools
from typing import TYPE_CHECKING, Union
from ..io import dirt
from ..sequences.Parsers import PatternParser

if TYPE_CHECKING:
    from ..clock import Clock


class OSCSender:

    def __init__(self,
            clock: "Clock",
            osc_client,
            address: str,
            at: Union[float, int] = 0,
            **kwargs):

        self.clock = clock
        self.osc_client = osc_client
        self.address = self._parse_osc_addresses(address)

        self.content = {}
        for key, value in kwargs.items():
            if isinstance(value, (int, float)):
                self.content[key] = value
            else:
                self.content[key] = self._parse(value)
        self.after: int = at

        # Iterating over kwargs. If parameter seems to refer to a
        # method (usually dynamic SuperDirt parameters), call it
        for k, v in kwargs.items():
            method = getattr(self, k, None)
            if callable(method):
                method(v)
            else:
                self.content[k] = v


    def _parse_osc_addresses(self, pattern: str):
        """Pre-parse OSC client pattern during __init__"""
        pat = PatternParser(pattern=pattern, type='address')
        return pat.pattern


    def _parse(self, pattern: str):
        """Pre-parse MIDI params during __init__"""
        pat = PatternParser(pattern=pattern, type='number')
        return pat.pattern


    def __str__(self):
        """String representation of a sender content"""
        param_dict = pprint.pformat(self.content)
        return f"{self.address}: {param_dict}"

    # ------------------------------------------------------------------------
    # GENERIC Mapper: make parameters chainable!

    def __getattr__(self, name: str):
        method = functools.partial(self.addOrChange, name=name)
        method.__doc__ = f"Updates the sound's {name} parameter."
        return method


    def addOrChange(self, values, name: str):
        """Will set a parameter or change it if already in message"""

        # Detect if a given parameter is a pattern, form a valid pattern
        if isinstance(values, (str)):
            self.content |= {name: self._parse(values)}
        return self


    def schedule(self, message: dict):
        async def _waiter():
            await handle
            print(message['message'])
            self.osc_client.send(
                    self.clock,
                    message['address'],
                    message['message'])

        ticks = self.clock.get_beat_ticks(self.after, sync=False)
        # Beat synchronization is disabled since `self.after`
        # is meant to offset us from the current time
        handle = self.clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name='osc-scheduler')

    def out(self, i: Union[int, None]) -> None:
        """Sender method"""

        final_message = {}
        def _message_without_iterator():
            """Compose a message if no iterator is given"""

            # Address
            if self.address == []:
                return
            if isinstance(self.address, list):
                final_message['address'] = self.address[0]
            elif isinstance(self.address, str):
                final_message['address'] = self.address[0]

            # Parametric values: names are mental helpers for the user
            final_message['message'] = []
            for _, value in self.content.items():
                if value == []:
                    continue
                if isinstance(value, list):
                    value = value[0]
                if _ != 'trig':
                    final_message['message'].append(float(value))

            if 'trig' not in self.content.keys():
                trig = 1
            else:
                trig = int(self.content['trig'][0])
            if trig:
                return self.schedule(final_message)

        def _message_with_iterator():
            """Compose a message if an iterator is given"""

            # Sound
            if self.address == []:
                return
            if isinstance(self.address, list):
                final_message['address'] = self.address[
                        i % len(self.address) - 1]
            else:
                final_message['address'] = self.address

            # Parametric arguments
            final_message['message'] = []
            for _, value in self.content.items():
                if value == []:
                    continue
                if isinstance(value, list):
                    value = float(value[i % len(value) - 1])
                    if _ != 'trig':
                        final_message['message'].append(value)
                else:
                    if _ != 'trig':
                        final_message['message'].append(float(value))

            if 'trig' not in self.content.keys():
                trig = 1
            else:
                trig = int(self.content['trig'][
                    i % len(self.content['trig']) -1])
            if trig:
                return self.schedule(final_message)

        # Composing and sending messages
        if i is None:
            return _message_without_iterator()
        else:
            return _message_with_iterator()
