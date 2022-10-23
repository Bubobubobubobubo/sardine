#!/usr/bin/env python3
import asyncio
import pprint
import functools
from typing import TYPE_CHECKING, Union
from ..io import dirt
from ..sequences import ListParser
from math import floor

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
        async def _waiter():
            await handle
            await asyncio.sleep(self._nudge)
            dirt(message)

        ticks = self.clock.get_beat_ticks(self.after, sync=False)
        # Beat synchronization is disabled since `self.after`
        # is meant to offset us from the current time
        handle = self.clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name="superdirt-scheduler")

    def _pattern_element(self, div: int, speed: int, iterator: int, pattern: list):
        """Joseph Enguehard's algorithm"""
        return floor(iterator * speed / div) % len(pattern)

    def out(self, i: int = 0, div: int = 1, speed: int = 1) -> None:
        """
        Prototype for the Sender output.
        """
        if self.clock.tick % div != 0:
            return

        # Value checking
        i = int(i)
        div = int(div) if div != 0 else self.clock.ppqn

        final_message = []

        def _message_without_iterator():
            """Compose a message if no iterator is given"""
            # Sound
            if self.sound == []:
                return
            if isinstance(self.sound, list):
                final_message.extend(["sound", self.sound[0]])
            elif isinstance(self.sound, str):
                final_message.extend(["sound", self.sound])

            # Parametric values
            for key, value in self.content.items():
                if value == []:
                    continue
                if isinstance(value, list):
                    value = value[0]
                final_message.extend([key, float(value)])

            if "trig" not in final_message:
                final_message.extend(["trig", 1])

            trig_value = final_message[final_message.index("trig") + 1]
            if trig_value:
                return self.schedule(final_message)

        def _message_with_iterator():
            """Compose a message if an iterator is given"""

            # Sound
            if self.sound == []:
                return
            if isinstance(self.sound, list):
                final_message.extend(
                    [
                        "sound",
                        self.sound[
                            self._pattern_element(
                                iterator=i, div=div, speed=speed, pattern=self.sound
                            )
                        ],
                    ]
                )
            else:
                final_message.extend(["sound", self.sound])

            # Parametric arguments
            for key, value in self.content.items():
                if value == []:
                    continue
                if isinstance(value, list):
                    value = float(
                        value[
                            self._pattern_element(
                                iterator=i, div=div, speed=speed, pattern=value
                            )
                        ]
                    )
                    final_message.extend([key, value])
                else:
                    final_message.extend([key, float(value)])

            if "trig" not in final_message:
                final_message.extend(["trig", str(1)])

            trig_value = final_message[final_message.index("trig") + 1]
            if trig_value:
                return self.schedule(final_message)

        # Composing and sending messages
        if i is None:
            return _message_without_iterator()
        else:
            return _message_with_iterator()
