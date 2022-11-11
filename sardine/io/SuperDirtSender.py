#!/usr/bin/env python3
import asyncio
import pprint
import functools
from typing import TYPE_CHECKING, Union
from ..io import dirt
from ..sequences import ListParser
from ..sequences.LexerParser.Chords import Chord
from .SenderLogic import pattern_element, compose_parametric_patterns

if TYPE_CHECKING:
    from ..clock import Clock


class SuperDirtSender:
    def __init__(
        self,
        clock: "Clock",
        sound: str,
        at: Union[float, int] = 0,
        nudge: Union[float, int] = 0.0,
        **kwargs,
    ):

        self.clock = clock
        self._general_parser = self.clock.parser
        self.sound = self._parse_sound(sound)
        self.after: int = at
        self._nudge: Union[float, int] = nudge

        # Iterating over kwargs. If parameter seems to refer to a
        # method (usually dynamic SuperDirt parameters), call it

        self.content = {"orbit": 0}
        for k, v in kwargs.items():
            method = getattr(self, k, None)
            if callable(method):
                method(v)

    def _parse_sound(self, sound_pattern: str):
        """Pre-parse sound param during __init__"""
        pat = self._general_parser.parse(sound_pattern)
        return pat

    def __str__(self):
        """String representation of a sender content"""
        param_dict = pprint.pformat(self.content)
        return f"{self.sound}: {param_dict}"

    def __getattr__(self, name: str):
        method = functools.partial(self.addOrChange, name=name)
        method.__doc__ = f"Updates the sound's {name} parameter."
        return method

    def addOrChange(self, values, name: str):
        """Will set a parameter or change it if already in message"""
        if isinstance(values, str):
            self.content |= {name: self._general_parser.parse(values)}
        else:
            self.content |= {name: values}
        return self

    def schedule(self, message):
        """
        Higher logic of the schedule function. Is able to send both monophonic
        and polyphonic messages.
        """
        # Analyse message to find chords lying around
        def chords_in_message(message: list) -> bool:
            return any(isinstance(x, Chord) for x in message)

        def longest_list_in_message(message: list) -> int:
            return max(len(x) if isinstance(x, (Chord, list)) else 1 for x in message)

        if chords_in_message(message):
            # We need to compose len(longest_list) messages
            longest_list = longest_list_in_message(message)
            list_of_messages = []
            for _ in range(0, longest_list):
                note_message = [
                    x if not isinstance(x, Chord) else x[_ % len(x)] for x in message
                ]
                list_of_messages.append(note_message)
            for message in list_of_messages:
                self._schedule(message)
        else:
            self._schedule(message)

    def _schedule(self, message):
        async def _waiter():
            await handle
            await asyncio.sleep(self._nudge)
            dirt(message, self.clock)

        ticks = self.clock.get_beat_ticks(self.after, sync=False)
        # Beat synchronization is disabled since `self.after`
        # is meant to offset us from the current time
        handle = self.clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name="superdirt-scheduler")

    def out(self, i: int = 0, div: int = 1, rate: int = 1) -> None:
        """
        Prototype for the Sender output.
        """
        if i % div != 0:
            return
        i = int(i)
        final_message = []

        def _message_without_iterator():
            """Compose a message if no iterator is given"""
            composite_tokens = (list, Chord)
            single_tokens = (type(None), str)

            # =================================================================
            # HANDLING THE SOUND PARAMETER
            # =================================================================

            if self.sound == []:
                return

            # Handling lists
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
            single_tokens = (type(None), str)

            # =================================================================
            # HANDLING THE SOUND PARAMETER
            # =================================================================

            if self.sound == []:
                return
            if isinstance(self.sound, list):
                new_element = self.sound[
                    pattern_element(iterator=i, div=div, rate=rate, pattern=self.sound)
                ]
                if new_element is None:
                    return
                else:
                    final_message.extend(["sound", new_element])
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
                final_message.extend(["trig", str(1)])

            trig_value = final_message[final_message.index("trig") + 1]
            if trig_value:
                return self.schedule(final_message)

        # Ultimately composing and sending message
        if i == 0:
            return _message_without_iterator()
        else:
            return _message_with_iterator()
