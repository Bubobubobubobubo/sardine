#!/usr/bin/env python3
import asyncio
import pprint
import functools
from typing import TYPE_CHECKING, Union
from ..io import dirt
from ..sequences.Parsers import PatternParser

if TYPE_CHECKING:
    from ..clock import Clock
    from ..io import MIDIIo


class MIDISender:

    def __init__(self,
            clock: 'Clock',
            midi_client: 'MIDIIo',
            velocity: Union[int, float, str] = 120,
            channel:  Union[int, float, str] = 0,
            at: Union[float, int] = 0,
            **kwargs):

        self.clock = clock
        self.midi_client = midi_client

        # Velocity parsing
        if isinstance(velocity, str):
            self.velocity = self.parse(velocity)
        else:
            self.velocity = velocity

        # Channel parsing
        if isinstance(channel, str):
            self.channel= self.parse(channel)
        else:
            self.channel= channel

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

    def parse(self, pattern: str):
        """Pre-parse MIDI params during __init__"""
        pat = PatternParser(pattern=pattern, type='number')
        return pat.pattern

    def __str__(self):
        """String representation of a sender content"""
        param_dict = pprint.pformat(self.content)
        return f"{self.midi_port}: {param_dict}"

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


    def willPlay(self) -> bool:
        """
        Return a boolean that will tell if the pattern is planned to be sent
        to SuperDirt or if it will be discarded.
        """
        return True if self.content.get('trig') == 1 else False


    def schedule(self, message):
        async def _waiter():
            await handle
            self.midi_client.send(Mido.message())
            dirt(message)


        ticks = self.clock.get_beat_ticks(self.after, sync=False)
        # Beat synchronization is disabled since `self.after`
        # is meant to offset us from the current time
        handle = self.clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name='superdirt-scheduler')


    def out(self) -> None:
        """Must be able to deal with polyphonic messages """
        if not self.willPlay():
            return

        final_message = {}
        def _message_without_iterator():
            """Compose a message if no iterator is given"""

            # Velocity
            if self.velocity == []:
                return
            if isinstance(self.velocity, list):
                final_message['velocity'] = self.velocity[0]
            elif isinstance(self.velocity, str):
                final_message['velocity'] = self.velocity[0]

            # Parametric values: names are mental helpers for the user
            final_message['message'] = []
            for _, value in self.content.items():
                if value == []:
                    continue
                if isinstance(value, list):
                    value = value[0]
                final_message['message'].append(float(value))

            return self.schedule(message=final_message)

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
                    final_message['message'].append(value)
                else:
                    final_message['message'].append(float(value))

            return self.schedule(message=final_message)

        # Composing and sending messages
        if i is None:
            return _message_without_iterator()
        else:
            return _message_with_iterator()
