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
            osc_client: str,
            address: str,
            at: Union[float, int] = 0,
            **kwargs):

        self.clock = clock
        self.osc_client = osc_client
        self.address = self._parse_osc_addresses(address)
        self.content = {}
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
        pat = PatternParser(pattern=pattern, type='sound')
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


    def out(self, orbit:int = 0) -> None:
        """Must be able to deal with polyphonic messages """

        # Specify a different orbit using the merge operator (Python 3.9)
        if orbit != 0:
            self.content |= {'orbit': orbit}

        if not self.willPlay():
            return

        common = []
        polyphonic_pairs: list[tuple[str, list]] = []

        # Discard the polyphonic messages thingie during refactoring

        # Separate polyphonic parameters from content
        # for i in range(0, len(self.content), 2):
        #     name: str
        #     name, value = self.content[i:i+2]
        #     if isinstance(value, list):
        #         polyphonic_pairs.append((name, value))
        #     else:
        #         common.extend((name, value))

        if not polyphonic_pairs:
            # Simple monophonic message need no care
            return self.schedule(common)

        # names, value_table = zip(*polyphonic_pairs)
        # max_values = max(len(values) for values in value_table)
        # tails: list[list] = []
        # for i in range(max_values):
        #     # if there is more than one polyphonic pair with differing
        #     # lengths, we will wrap around
        #     zipping_values = (values[i % len(values)] for values in value_table)

        #     tail = []
        #     for pair in zip(names, zipping_values):
        #         tail.extend(pair)
        #     tails.append(tail)

        # for i in tails:
        #     self.schedule(common + i)
