#!/usr/bin/env python3
import asyncio
import functools
from typing import TYPE_CHECKING, Union

from ..io import dirt

if TYPE_CHECKING:
    from ..clock import Clock

__all__ = ("SuperDirt",)


class SuperDirt:
    def __init__(self, clock: "Clock", sound: str, at: Union[float, int] = 0, **kwargs):
        self.clock = clock
        # Default message when triggering soundfile/synth
        self.content = ["orbit", 0, "trig", 1, "sound", sound]
        self.after: int = at

        # Iterating over kwargs. If parameter seems to refer to a
        # method (usually dynamic SuperDirt parameters), call it
        for k, v in kwargs.items():
            method = getattr(self, k, None)
            if callable(method):
                method(v)

    def __str__(self):
        return " ".join(str(e) for e in self.content)

    # ------------------------------------------------------------------------
    # GENERIC Mapper: make parameters chainable!

    def __getattr__(self, name: str):
        method = functools.partial(self.addOrChange, name=name)
        method.__doc__ = f"Updates the sound's {name} parameter."
        return method

    def addOrChange(self, value, name: str):
        """Will set a parameter or change it if already in message"""
        try:
            i = self.content.index(name)
        except ValueError:
            self.content.extend((name, value))
        else:
            self.content[i + 1] = value

        return self

    def query_existing_value(self, index: str) -> Union[int, float]:
        "Find the value associated to a name. Return false if not found."
        try:
            posIndex = self.content.index(index)
        except ValueError:
            raise ValueError("can't query existing value {index}")
        return self.content[posIndex + 1]

    def change_existing_value(self, index: str, new_value: Union[int, float]) -> None:
        "Change the value associated to a name."
        try:
            valueIndex = self.content.index(index)
        except ValueError:
            return
        self.content[valueIndex + 1] = new_value

    def n(self, number: int = 0) -> None:
        """Change the number of the selected sample"""
        if not isinstance(number, (int, float)):
            return
        current_value = self.query_existing_value("sound")
        if ":" in list(current_value):
            self.change_existing_value(
                index="sound",
                new_value=current_value.split(":")[0] + str(f":{int(number)}"),
            )
        else:
            self.change_existing_value(
                index="sound", new_value=current_value + str(f":{int(number)}")
            )

    def willPlay(self) -> bool:
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
        asyncio.create_task(_waiter(), name="superdirt-scheduler")

    def out(self, orbit: int = 0) -> None:
        """Must be able to deal with polyphonic messages"""

        # It is now possible to specify the orbit in this function.
        if orbit != 0:
            self.change_existing_value("orbit", orbit)

        if not self.willPlay():
            return

        common = []
        polyphonic_pairs: list[tuple[str, list]] = []

        # Separate polyphonic parameters from content
        for i in range(0, len(self.content), 2):
            name: str
            name, value = self.content[i : i + 2]
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
