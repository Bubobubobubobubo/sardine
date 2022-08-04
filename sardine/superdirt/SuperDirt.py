#!/usr/bin/env python3
import asyncio
import functools
from typing import TYPE_CHECKING, Union

from ..io import dirt

if TYPE_CHECKING:
    from ..clock import Clock

__all__ = ('SuperDirt',)


class SuperDirt:

    def __init__(
        self,
        clock: "Clock",
        sound: str,
        at: Union[float, int] = 0,
        **kwargs
    ):
        self.clock = clock
        # Default message when triggering soundfile/synth
        self.content = ["orbit", 0, "trig", 1, "sound", sound]
        self.after: int = at

        # Iterating over kwargs. If parameter seems to refer to a
        # method (usually dynamic SuperDirt parameters), call it
        for k, v in kwargs.items():
            method = getattr(self, k, None)
            if callable(method):
                method(v)

        # for key, value in kwargs.items():
        #     if key in self._mono_param_list:
        #         self.setorChangeMonoParam(key, value)
        #     else:
        #         # Is there a method in this class that can handle it?
        #         method = getattr(self, key, None)
        #         if callable(method):
        #             # calling the given method with the given value
        #             method(value)

        # self.generate_chainable_methods(params)

    def __str__(self):
        return ' '.join(str(e) for e in self.content)

    # ------------------------------------------------------------------------
    # GENERIC Mapper: make parameters chainable!

    def __getattr__(self, name: str):
        method = functools.partial(self.addOrChange, name=name)
        method.__doc__ = f"Updates the sound's {name} parameter."
        return method

    # def _generic_mapper(self, amount, name: str):
    #     self.addOrChange(name, amount)
    #     return self

    # def generate_chainable_methods(self, params: list):
    #     for param in params:
    #         setattr(self, param, partial(self._generic_mapper, name=param))

    def addOrChange(self, value, name: str):
        """Will set a parameter or change it if already in message """
        try:
            i = self.content.index(name)
        except ValueError:
            self.content.extend((name, value))
        else:
            self.content[i + 1] = value

        return self

    def query_existing_value(self, index):
        "Find the value associated to a name. Return false if not found."
        try:
            posIndex = self.content.index(index)
        except ValueError:
            return False
        return self.content[posIndex + 1]

    def change_existing_value(self, index, new_value):
        "Change the value associated to a name."
        try:
            valueIndex = self.content.index(index)
        except ValueError:
            return
        self.content[valueIndex + 1] = new_value

    def willPlay(self):
        """
        Return a boolean that will tell if the pattern is planned to be sent
        to SuperDirt or if it will be discarded.
        """
        return True if self.query_existing_value("trig") == 1 else False

    def schedule(self, message):
        async def _waiter():
            await handle
            dirt(message)

        ticks = self.clock.get_beat_ticks(self.after, sync=False)
        # Beat synchronization is disabled since `self.after`
        # is meant to offset us from the current time
        handle = self.clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name='superdirt-scheduler')

    def out(self, output=0):
        """Must be able to deal with polyphonic messages """

        # It is now possible to specify the orbit in this function.
        if output != 0: self.change_existing_value("orbit", output)

        if not self.willPlay():
            return

        common = []
        polyphonic_pairs: list[tuple[str, list]] = []

        # Separate polyphonic parameters from content
        for i in range(0, len(self.content), 2):
            name: str
            name, value = self.content[i:i+2]
            if isinstance(value, list):
                polyphonic_pairs.append((name, value))
            else:
                common.extend((name, value))

        if not polyphonic_pairs:
            # Simple monophonic message need no care
            return self.schedule(common)

        names, value_table = zip(*polyphonic_pairs)
        max_values = max(len(values) for values in value_table)
        tails: list[list] = []
        for i in range(max_values):
            # if there is more than one polyphonic pair with differing
            # lengths, we will wrap around
            zipping_values = (values[i % len(values)] for values in value_table)

            tail = []
            for pair in zip(names, zipping_values):
                tail.extend(pair)
            tails.append(tail)

        for i in tails:
            self.schedule(common + i)
