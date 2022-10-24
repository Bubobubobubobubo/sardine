#!/usr/bin/env python3
import asyncio
import pprint
import functools
from typing import TYPE_CHECKING, Union
from ..io import dirt
from ..sequences import ListParser
from math import floor
from .SenderLogic import (pattern_element, compose_parametric_patterns)

if TYPE_CHECKING:
    from ..clock import Clock


class OSCSender:
    def __init__(
        self,
        clock: "Clock",
        osc_client,
        address: str,
        at: Union[float, int] = 0,
        **kwargs,
    ):

        self.clock = clock
        self._number_parser, self._name_parser = (self.clock.parser, self.clock.parser)
        self.osc_client = osc_client
        self.address = self._name_parser.parse(address)

        self.content = {}
        for key, value in kwargs.items():
            if isinstance(value, (int, float)):
                self.content[key] = value
            else:
                self.content[key] = self._number_parser.parse(value)
        self.after: int = at

        # Iterating over kwargs. If parameter seems to refer to a
        # method (usually dynamic SuperDirt parameters), call it
        for k, v in kwargs.items():
            method = getattr(self, k, None)
            if callable(method):
                method(v)
            else:
                self.content[k] = v

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

        # Detect if a given parameter is a pattern, form a valid pattern
        if isinstance(values, (str)):
            self.content |= {name: self._number_parser.parse(values)}
        return self

    def schedule(self, message: dict):
        async def _waiter():
            await handle
            self.osc_client.send(self.clock, message["address"], message["message"])

        ticks = self.clock.get_beat_ticks(self.after, sync=False)
        # Beat synchronization is disabled since `self.after`
        # is meant to offset us from the current time
        handle = self.clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name="osc-scheduler")

    def out(self, i: int = 0, div: int = 1, speed: int = 1) -> None:
        """Sender method"""

        if self.clock.tick % div != 0:
            return

        final_message = {}

        i = int(i)

        def convert_list_to_dict(lst):
            res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
            return res_dct

        def _message_without_iterator():
            """Compose a message if no iterator is given. This will simply
            return the first value from every pattern, except for silence. 
            Silence will return nothing."""

            # This is the case where nothing is returned
            if self.address == [] or self.address[0] is None:
                return
            if isinstance(self.address, (list, str)):
                given_address = self.address[0]
                if given_address is None:
                    return
                else:
                    final_message["address"] = "/" + given_address

            # We now have the address and we move to the content of the message
            # We will store the final message inside a list
            final_message["message"] = []

            # Browsing items and figuring out what the first value is
            for key, value in self.content.items():
                if value == []:
                    continue
                if isinstance(value, list):
                    given_value = value[0]
                    if given_value is None:
                        return
                    else:
                        if key != 'trig':
                            final_message["message"].append(value)

            if "trig" not in self.content.keys():
                trig = 1
            else:
                trig = int(self.content["trig"][0])
            if trig:
                return self.schedule(final_message)


        def _message_with_iterator():
            """Compose a message if an iterator is given"""

            if "trig" not in self.content.keys():
                self.content['trig'] = 1

            # We need to determine the address, given that 
            # the address can also be a silence.
            if self.address == []:
                return
            if isinstance(self.address, list):
                new_element = self.address[pattern_element(
                    iterator=i, div=div, 
                    speed=speed, 
                    pattern=self.address)]
                if new_element is None:
                    return
                else:
                    final_message["address"] = "/" + new_element
            else:
                final_message["address"] = "/" + self.address

            # Now that we have it, we will iterate over pattern arguments to 
            # form the message, just like in the non-iterated version

            final_message["message"] = []
            pattern_result = compose_parametric_patterns(
                    div=div, speed=speed, iterator=i, 
                    items=self.content.items())
            print(type(pattern_result), pattern_result)
            final_message["message"].extend(pattern_result)

            # Now we have to an enormous operation just to check on trig...
            if isinstance(self.content['trig'], list):
                trig = self.content["trig"][
                    pattern_element(
                        iterator=i, div=div, 
                        speed=speed, pattern=self.content["trig"]) ]
                if trig is None:
                    for decreasing_index in range(i, -1, -1):
                        trig = self.content['trig'][
                            pattern_element(
                                iterator=decreasing_index,
                                div=div,
                                speed=speed,
                                pattern=self.content['trig'])]
                        if trig is None:
                            continue
                        else:
                            trig = int(trig)
                            break
                    if trig is None:
                        raise ValueError("Pattern does not contain any value")
                else:
                    trig = int(trig)
            elif isinstance(self.content['trig'], (int, float, str)):
                trig = int(self.content['trig'])

            if trig:
                return self.schedule(final_message)

        # Ultimately composing and sending message
        if i is None:
            return _message_without_iterator()
        else:
            return _message_with_iterator()
