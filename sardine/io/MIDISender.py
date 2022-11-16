#!/usr/bin/env python3
import asyncio
from email import parser
import pprint
import functools
from typing import TYPE_CHECKING, Union, Optional
from ..sequences import ListParser
from math import floor
from .SenderLogic import pattern_element, compose_parametric_patterns
from ..sequences.LexerParser.Chords import Chord

if TYPE_CHECKING:
    from ..legacy import Clock
    from ..io import MIDIIo


class MIDISender:
    def __init__(
        self,
        clock: "Clock",
        midi_client: Optional["MIDIIo"] = None,
        note: Union[int, float, str, Chord] = 60,
        delay: Union[int, float, str, Chord] = 0.1,
        velocity: Union[int, float, str, Chord] = 120,
        channel: Union[int, float, str, Chord] = 0,
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
        """
        Higher logic of the schedule function. Is able to send both monophonic
        and polyphonic messages
        """
        # Analyse message to find chords lying around
        def chords_in_message(message: list) -> bool:
            return any(isinstance(x, Chord) for x in message)

        def longest_list_in_message(message: list) -> int:
            return max(len(x) if isinstance(x, (Chord, list)) else 1 for x in message)

        def clamp_everything_to_midi_range(message: list) -> list:
            """Clamp every value to MIDI Range (0-127)"""

            def _clamp(n, smallest, largest):
                return max(smallest, min(n, largest))

            new_list = []
            for _ in message:
                if isinstance(_, str):
                    new_list.append(_)
                elif isinstance(_, (float, int)):
                    new_list.append(_clamp(_, 0, 127))
                elif isinstance(_, Chord):
                    new_list.append(_._clamp())
                else:
                    new_list.append(_)
            return new_list

        # Clamping values for safety
        message = clamp_everything_to_midi_range(message)

        if chords_in_message(message):
            # We need to compose len(longest_list) messages
            longest_list = longest_list_in_message(message)
            list_of_messages = []
            for _ in range(0, longest_list):
                note_message = [
                    x if not isinstance(x, Chord) else x[_] for x in message
                ]
                list_of_messages.append(note_message)
            for message in list_of_messages:
                self._schedule(dict(zip(message[::2], message[1::2])))
        else:
            self._schedule(dict(zip(message[::2], message[1::2])))

    def _schedule(self, message):
        async def _waiter():
            await asyncio.sleep(self._nudge)
            await handle
            asyncio.create_task(
                self.midi_client.note(
                    delay=message.get("delay"),
                    note=int(message.get("sound")),
                    velocity=int(message.get("velocity")),
                    channel=int(message.get("channel")),
                )
            )

        ticks = self.clock.get_beat_ticks(self.after, sync=True)
        # Beat synchronization is disabled since `self.after`
        # is meant to offset us from the current time
        handle = self.clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name="midi-scheduler")

    def out(self, i: int = 0, div: int = 1, rate: int = 1) -> None:
        """
        Prototype for the Sender output.
        """
        if i % div != 0:
            return
        i = int(i)
        final_message = []

        # Mimicking the SuperDirtSender behavior
        self.sound = self.note
        self.content |= {
            "delay": self.delay,
            "velocity": self.velocity,
            "channel": self.channel,
            "trig": self.trig,
        }

        def _message_without_iterator():
            """Compose a message if no iterator is given"""
            composite_tokens = (list, Chord)
            single_tokens = (type(None), str, int, float)

            # =================================================================
            # HANDLING THE SOUND PARAMETER
            # =================================================================

            if self.sound == []:
                return

            # Handling lists and chords
            if isinstance(self.sound, composite_tokens):
                first_element = self.sound[0]
                if first_element is not None:
                    final_message.extend(["sound", self.sound[0]])
                else:
                    return
            # Handling other representations (str, None)
            elif isinstance(self.sound, single_tokens):
                if self.sound is None:
                    return
                else:
                    final_message.extend(["sound", self.sound])

            # =================================================================
            # HANDLING OTHER PARAMETERS
            # =================================================================

            # Handling other non-essential keys
            for key, value in self.content.items():
                # We don't care if there is no value, just drop it
                if value == []:
                    continue
                if isinstance(value, composite_tokens):
                    value = value[0]
                final_message.extend([key, value])

            # =================================================================
            # TRIGGER MANAGEMENT
            # =================================================================

            if "trig" not in final_message:
                final_message.extend(["trig", 1])

            trig_value = final_message[final_message.index("trig") + 1]
            if trig_value:
                return self.schedule(final_message)

        def _message_with_iterator():
            """Compose a message if an iterator is given"""
            composite_tokens = (list, Chord)
            single_tokens = (type(None), str, float, int)

            # =================================================================
            # HANDLING THE SOUND PARAMETER
            # =================================================================
            if self.sound == []:
                return
            if isinstance(self.sound, composite_tokens):
                new_element = self.sound[
                    pattern_element(iterator=i, div=div, rate=rate, pattern=self.sound)
                ]
                if new_element is None:
                    return
                else:
                    final_message.extend(["sound", new_element])
            elif isinstance(self.sound, single_tokens):
                if self.sound is None:
                    return
                else:
                    final_message.extend(["sound", self.sound])
            else:
                if self.sound is None:
                    return
                else:
                    final_message.extend(["sound", self.sound])

            # =================================================================
            # HANDLING OTHER PARAMETERS
            # =================================================================

            pattern_result = compose_parametric_patterns(
                div=div, rate=rate, iterator=i, items=self.content.items()
            )
            final_message.extend(pattern_result)

            # =================================================================
            # TRIGGER MANAGEMENT
            # =================================================================

            # Trig must always be included
            if "trig" not in final_message:
                final_message.extend(["trig", 1])

            trig_value = final_message[final_message.index("trig") + 1]
            if trig_value:
                return self.schedule(final_message)

        # Ultimately composing and sending message
        if i == 0:
            return _message_without_iterator()
        else:
            return _message_with_iterator()
