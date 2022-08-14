#!/usr/bin/env python3
import asyncio
import pprint
import functools
from typing import TYPE_CHECKING, Union, Optional
from ..io import dirt
from ..sequences.Parsers import PatternParser

if TYPE_CHECKING:
    from ..clock import Clock
    from ..io import MIDIIo


class MIDISender:

    def __init__(self,
            clock: 'Clock',
            midi_client: Optional['MIDIIo'] = None,
            note: Union[int, float, str] = 60,
            delay: Union[int, float, str] = 0.1,
            velocity: Union[int, float, str] = 120,
            channel:  Union[int, float, str] = 0,
            at: Union[float, int] = 0):

        self.clock = clock
        if midi_client is None:
            self.midi_client = self.clock._midi
        else:
            self.midi_client = midi_client

        # Delay parsing [1]
        if isinstance(delay, str):
            self.delay = self.parse(delay)
        else:
            self.delay = delay

        # Velocity parsing [2]
        if isinstance(velocity, str):
            self.velocity = self.parse(velocity)
        else:
            self.velocity = velocity

        # Channel parsing [3]
        if isinstance(channel, str):
            self.channel= self.parse(channel)
        else:
            self.channel= channel


        # Note parsing [3]
        if isinstance(note, str):
            self.note = self.parse(note)
        else:
            self.note = note

        self.after: int = at

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


    def schedule(self, message):
        async def _waiter():
            await handle
            asyncio.create_task(self.midi_client.note(
                delay=message.get('delay'),
                note=message.get('note'),
                velocity=message.get('velocity'),
                channel=message.get('channel')))


        ticks = self.clock.get_beat_ticks(self.after, sync=False)
        # Beat synchronization is disabled since `self.after`
        # is meant to offset us from the current time
        handle = self.clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name='midi-scheduler')


    def out(self, i: Union[int, None]) -> None:
        """Must be able to deal with polyphonic messages """
        final_message = {
                'delay': self.delay,
                'velocity': self.velocity,
                'channel': self.channel,
                'note': self.note}

        def _message_without_iterator():
            """Compose a message if no iterator is given"""

            for key, value in final_message.items():
                if value == []: return
                if isinstance(value, (list, str)):
                    final_message[key] = int(value[0])

            return self.schedule(message=final_message)

        def _message_with_iterator():
            """Compose a message if an iterator is given"""

            for key, value in final_message.items():
                if value == []: return
                if isinstance(value, (list, str)):
                    final_message[key] = int(value[i % len(value) - 1])

            return self.schedule(message=final_message)

        # Composing and sending messages
        if i is None:
            return _message_without_iterator()
        else:
            return _message_with_iterator()
