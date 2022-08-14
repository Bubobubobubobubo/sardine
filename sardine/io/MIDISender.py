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
            trig:  Union[int, float, str] = 1,
            at: Union[float, int] = 0):

        self.clock = clock
        if midi_client is None:
            self.midi_client = self.clock._midi
        else:
            self.midi_client = midi_client

        self.trig = self.parse_initial_arguments(trig)
        self.delay = self.parse_initial_arguments(delay)
        self.velocity = self.parse_initial_arguments(velocity)
        self.channel = self.parse_initial_arguments(channel)
        self.note = self.parse_initial_arguments(note)
        self.after: int = at


    def parse_initial_arguments(self, argument):
        """Parse arguments at __init__ time """
        if isinstance(argument, str):
            return self._parse_number_pattern(argument)
        else:
            return argument


    def _parse_number_pattern(self, pattern: str):
        """Pre-parse MIDI params during __init__"""
        pat = PatternParser(pattern=pattern, type='number')
        return pat.pattern


    def __str__(self):
        """String representation of a sender content"""
        pat = {'note': self.note,
               'delay': self.delay,
               'velocity': self.velocity,
               'channel': self.channel}
        return f"{self.midi_port}: {pprint.pformat(pat)}"

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


    def out(self, i: Union[int, None]=None) -> None:
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
                    if key in ['velocity', 'channel', 'note']:
                        final_message[key] = int(value[0])
                    else:
                        final_message[key] = float(value[0])

            if isinstance(self.trig, list):
                self.trig = self.trig.pop(0)
            else:
                self.trig = int(self.trig)
            if self.trig:
                return self.schedule(message=final_message)

        def _message_with_iterator():
            """Compose a message if an iterator is given"""

            for key, value in final_message.items():
                if value == []: return
                if isinstance(value, (list, str)):
                    if key in ['velocity', 'channel', 'note']:
                        final_message[key] = int(value[i % len(value) - 1])
                    else:
                        final_message[key] = float(value[i % len(value) - 1])

            if isinstance(self.trig, list):
                self.trig = self.trig[i % len(self.trig) - 1]
            else:
                self.trig = int(self.trig)
            if self.trig:
                return self.schedule(message=final_message)

        # Composing and sending messages
        if i is None:
            return _message_without_iterator()
        else:
            return _message_with_iterator()
