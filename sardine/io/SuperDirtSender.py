#!/usr/bin/env python3
import asyncio
import pprint
import functools
from typing import TYPE_CHECKING, Union
from ..io import dirt
from ..sequences.Parsers import PatternParser

if TYPE_CHECKING:
    from ..clock import Clock

class SuperDirtSender:

    def __init__(self, clock: "Clock", sound: str,
            at: Union[float, int] = 0, **kwargs):

        self.clock = clock
        self.sound = self._parse_sound(sound)
        self.after: int = at

        # Iterating over kwargs. If parameter seems to refer to a
        # method (usually dynamic SuperDirt parameters), call it

        self.content = {'orbit': 0, 'trig': 1}
        for k, v in kwargs.items():
            method = getattr(self, k, None)
            if callable(method):
                method(v)


    def _parse_sound(self, sound: str):
        """Pre-parse sound param during __init__"""
        pat = PatternParser(pattern=sound, type='sound')
        return pat.pattern


    def _parse_value(self, sound: str):
        """Pre-parse value param during __init__"""
        pat = PatternParser(pattern=sound, type='number')
        return pat.pattern

    def __str__(self):
        """String representation of a sender content"""
        param_dict = pprint.pformat(self.content)
        return f"{self.sound}: {param_dict}"

    # ------------------------------------------------------------------------
    # GENERIC Mapper: make parameters chainable!

    def __getattr__(self, name: str):
        method = functools.partial(self.addOrChange, name=name)
        method.__doc__ = f"Updates the sound's {name} parameter."
        return method


    def addOrChange(self, values, name: str):
        """Will set a parameter or change it if already in message"""
        # Detect if a given parameter is a pattern, form a valid pattern
        if isinstance(values, str):
            self.content |= {name: self._parse_value(values)}
        else:
            self.content |= {name: values}
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
            dirt(message)

        ticks = self.clock.get_beat_ticks(self.after, sync=False)
        # Beat synchronization is disabled since `self.after`
        # is meant to offset us from the current time
        handle = self.clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name='superdirt-scheduler')


    def out(self, orbit:int = 0, i: Union[None, int] = None) -> None:
        """Prototype for the Sender output"""
        if not self.willPlay():
            return

        if orbit != 0:
            self.content |= {'orbit': orbit}

        final_message = []

        def _message_without_iterator():
            """Compose a message if no iterator is given"""
            # Sound
            if self.sound == []:
                return
            if isinstance(self.sound, list):
                final_message.extend(['sound', self.sound[0]])
            elif isinstance(self.sound, str):
                final_message.extend(['sound', self.sound])

            # Parametric values
            for key, value in self.content.items():
                if value == []:
                    continue
                if isinstance(value, list):
                    value = value[0]
                final_message.extend([key, float(value)])
            return self.schedule(final_message)

        def _message_with_iterator():
            """Compose a message if an iterator is given"""

            # Sound
            if self.sound == []:
                return
            if isinstance(self.sound, list):
                final_message.extend(['sound',
                        self.sound[i % len(self.sound) - 1]])
            else:
                final_message.extend(['sound', self.sound])

            # Parametric arguments
            for key, value in self.content.items():
                if value == []:
                    continue
                if isinstance(value, list):
                    value = float(value[i % len(value) - 1])
                    final_message.extend([key, value])
                else:
                    final_message.extend([key, float(value)])

            return self.schedule(final_message)


        # Composing and sending messages
        if i is None:
            return _message_without_iterator()
        else:
            return _message_with_iterator()


    # def out(self, orbit:int = 0, iterator=Union[None, int]= None) -> None:
    #     """Must be able to deal with polyphonic messages """
    #     if not self.willPlay():
    #         return

    #     # Specify a different orbit using the merge operator (Python 3.9)
    #     if orbit != 0:
    #         self.content |= {'orbit': orbit}


    #     common = []
    #     polyphonic_pairs: list[tuple[str, list]] = []

    #     # Discard the polyphonic messages thingie during refactoring

    #     # Separate polyphonic parameters from content
    #     # for i in range(0, len(self.content), 2):
    #     #     name: str
    #     #     name, value = self.content[i:i+2]
    #     #     if isinstance(value, list):
    #     #         polyphonic_pairs.append((name, value))
    #     #     else:
    #     #         common.extend((name, value))

    #     if not polyphonic_pairs:
    #         # Simple monophonic message need no care
    #         return self.schedule(common)

    #     # names, value_table = zip(*polyphonic_pairs)
    #     # max_values = max(len(values) for values in value_table)
    #     # tails: list[list] = []
    #     # for i in range(max_values):
    #     #     # if there is more than one polyphonic pair with differing
    #     #     # lengths, we will wrap around
    #     #     zipping_values = (values[i % len(values)] for values in value_table)

    #     #     tail = []
    #     #     for pair in zip(names, zipping_values):
    #     #         tail.extend(pair)
    #     #     tails.append(tail)

    #     # for i in tails:
    #     #     self.schedule(common + i)
