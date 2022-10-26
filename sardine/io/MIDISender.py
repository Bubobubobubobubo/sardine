#!/usr/bin/env python3
import asyncio
from email import parser
import pprint
import functools
from typing import TYPE_CHECKING, Union, Optional
from ..io import dirt
from ..sequences import ListParser
from math import floor
from .SenderLogic import (pattern_element, compose_parametric_patterns)

if TYPE_CHECKING:
    from ..clock import Clock
    from ..io import MIDIIo


class MIDISender:
    def __init__(
        self,
        clock: "Clock",
        midi_client: Optional["MIDIIo"] = None,
        note: Union[int, float, str] = 60,
        delay: Union[int, float, str] = 0.1,
        velocity: Union[int, float, str] = 120,
        channel: Union[int, float, str] = 0,
        trig: Union[int, float, str] = 1,
        at: Union[float, int] = 0,
        nudge: Union[int, float] = 0.0,
    ):

        self.clock = clock
        self._number_parser, self._note_parser = (self.clock.parser, self.clock.parser)
        self.content = {}

        if midi_client is None:
            self.midi_client = self.clock._midi
        else:
            self.midi_client = midi_client

        self.trig = self.parse_initial_arguments(trig)
        self.delay = self.parse_initial_arguments(delay)
        self.velocity = self.parse_initial_arguments(velocity)
        self.channel = self.parse_initial_arguments(channel)
        self.note = self.parse_note(note)
        self.after: int = at
        self._nudge: Union[int, float] = nudge

    def parse_initial_arguments(self, argument):
        """Parse arguments at __init__ time"""
        if isinstance(argument, str):
            return self._parse_number_pattern(argument)
        else:
            return argument

    def parse_note(self, argument):
        """Parse arguments at __init__ time"""
        if isinstance(argument, str):
            return self._note_parser.parse(argument)
        else:
            return argument

    def _parse_number_pattern(self, pattern: str):
        """Pre-parse MIDI params during __init__"""
        return self._number_parser.parse(pattern)

    def __str__(self):
        """String representation of a sender content"""
        pat = {
            "note": int(self.note),
            "delay": self.delay,
            "velocity": int(self.velocity),
            "channel": int(self.channel),
        }
        return f"{self.midi_client}: {pprint.pformat(pat)}"

    # ------------------------------------------------------------------------
    # GENERIC Mapper: make parameters chainable!

    def schedule(self, message):
        async def _waiter():
            await asyncio.sleep(self._nudge)
            await handle
            asyncio.create_task(
                self.midi_client.note(
                    delay=message.get("delay"),
                    note=int(message.get("note")),
                    velocity=int(message.get("velocity")),
                    channel=int(message.get("channel")),
                )
            )

        ticks = self.clock.get_beat_ticks(self.after, sync=True)
        # Beat synchronization is disabled since `self.after`
        # is meant to offset us from the current time
        handle = self.clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name="midi-scheduler")

    def out(self, i: int = 0, div: int = 1, speed: int = 1) -> None:
        """Must be able to deal with polyphonic messages"""
        if i % div != 0:
            return

        i = int(i)
        self.content |= {
                "delay": self.delay,
                "velocity": self.velocity,
                "channel": self.channel}

        final_message = []

        def convert_list_to_dict(lst):
            res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
            return res_dct

        def wrap_midinote_in_range(note: int):
            if note > 127:
                note = 127
            if note < 0:
                note = 0
            return note

        def _message_without_iterator():
            """Compose a message if no iterator is given"""

            if self.note == []:
                return
            if isinstance(self.note, list):
                new_element = self.note[pattern_element(
                    iterator=i, div=div, speed=speed, pattern=self.note)]
                if new_element is None:
                    return
                else:
                    final_message.extend( ["note", wrap_midinote_in_range(new_element)])
            else:
                if self.note is None:
                    return
                else:
                    final_message.extend(["note", wrap_midinote_in_range(self.note)])

            # Parametric values
            for key, value in self.content.items():
                if value == []:
                    continue
                if isinstance(value, list):
                    if key == 'delay':
                        value = float(value[0])
                    else:
                        value = int(value[0])
                final_message.extend([key, float(value)])

            if "trig" not in final_message:
                final_message.extend(["trig", 1])

            trig_value = final_message[final_message.index("trig") + 1]
            if trig_value:
                return self.schedule(convert_list_to_dict(final_message))

        def _message_with_iterator():
            """Compose a message if an iterator is given"""

            # Decompose between note argument and other arguments
            # Note is the most important because it can impose silence

            if self.note == []:
                return
            if isinstance(self.note, list):
                new_element = self.note[pattern_element(
                    iterator=i, div=div, speed=speed, pattern=self.note)]
                if new_element is None:
                    return
                else:
                    final_message.extend( ["note", 
                        wrap_midinote_in_range(new_element)])
            else:
                if self.note is None:
                    return
                else:
                    final_message.extend(["note", 
                        wrap_midinote_in_range(self.note)])

            # Parametric arguments
            pattern_result = compose_parametric_patterns(
                    div=div, speed=speed, iterator=i,
                    cast_to_int=True,
                    midi_overflow_protection=True,
                    items=self.content.items())
            final_message.extend(pattern_result)
            note_silence = final_message[final_message.index("note") + 1] is None
            if note_silence:
                return

            # Trig must always be included
            if "trig" not in final_message:
                final_message.extend(["trig", str(1)])

            trig_value = final_message[final_message.index("trig") + 1]
            if trig_value:
                return self.schedule(convert_list_to_dict(final_message))

        # Ultimately composing and sending message
        if i == 0:
            return _message_without_iterator()
        else:
            return _message_with_iterator()
