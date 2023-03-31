import asyncio
from math import floor
from random import random
from typing import Callable, Generator, ParamSpec, TypeVar, Union, Optional
from ..base import BaseHandler
from ..utils import maybe_coro
from ..sequences import euclid


__all__ = ("Sender",)

P = ParamSpec("P")
T = TypeVar("T")

Number = Union[float, int]
ReducedElement = TypeVar("ReducedElement")
RecursiveElement = Union[ReducedElement, list]  # assume list is list[RecursiveElement]
ParsableElement = Union[RecursiveElement, str]

# Sub-types of ParsableElement
NumericElement = Union[Number, list, str]
StringElement = Union[str, list]  # assume list is list[StringElement]

Pattern = dict[str, list[ParsableElement]]
ReducedPattern = dict[str, ReducedElement]


def _maybe_index(val: RecursiveElement, i: int) -> RecursiveElement:
    if not isinstance(val, list):
        return val

    length = len(val)
    return val[i % length]


def _maybe_length(val: RecursiveElement) -> int:
    if isinstance(val, list):
        return len(val)
    return 0


class Sender(BaseHandler):

    """
    Handlers can inherit from 'Sender' if they are in charge of some output operation.
    Output operations in Sardine generally involve some amount of pattern parsing and
    monophonic/polyphonic message composition. This class implements most of the inter-
    nal behavior necessary for patterning. Each handler rely on these methods in the
    final 'send' method called by the user.

    pattern_element: return the right index number for the pattern.
    reduce_polyphonic_message: turn any dict pattern into a list of patterns.
    pattern_reduce: reduce a pattern to a dictionary of values corresponding to iterator
                    index.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timed_tasks: set[asyncio.Task] = set()

    def call_timed(
        self,
        deadline: float,
        func: Callable[P, T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        """Schedules the given (a)synchronous function to be called.

        Senders should always use this method to properly account for time shift.
        """

        async def scheduled_func():
            await self.env.sleeper.sleep_until(deadline)
            await maybe_coro(func, *args, **kwargs)

        task = asyncio.create_task(scheduled_func())
        self._timed_tasks.add(task)
        task.add_done_callback(self._timed_tasks.discard)

    @staticmethod
    def pattern_element(
        val: RecursiveElement,
        iterator: Number,
        divisor: Number,
        rate: Number,
    ) -> RecursiveElement:
        """Joseph Enguehard's algorithm for solving iteration speed"""
        # For simplicity, we're allowing non-sequences to be passed through
        if not isinstance(val, list):
            return val

        length = len(val)
        if length > 0:
            i = floor(iterator * rate / divisor) % length
            return val[i]
        raise ValueError(f"Cannot pattern an empty sequence: {val!r}")

    def pattern_reduce(
        self,
        pattern: Pattern,
        iterator: Number,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        *,
        use_divisor_to_skip: bool = True,
    ) -> Generator[ReducedPattern, None, None]:
        """Reduces a pattern to an iterator yielding subpatterns.

        First, any string values are parsed using the fish bowl's parser.
        Afterwards, if the pattern is a dictionary where none of its values
        are lists, the pattern is wrapped in a list and returned, ignoring
        the iterator/divisor/rate parameters. For example::

            >>> pat = {"note": 60, "velocity": 100}
            >>> list(sender.pattern_reduce(pat, 0, 1, 1))
            [{'note': 60, 'velocity': 100}]

        If it is a monophonic pattern, i.e. a dictionary where one or more
        of its values are lists, the corresponding element of those lists
        are indexed using the `pattern_element()` method which implements
        Joseph Enguehard's algorithm::

            >>> pat = {"note": [60, 70, 80, 90], "velocity": 100}
            >>> for i in range(1, 4):
            ...     list(sender.pattern_reduce(pat, i, 2, 3))
            [{'note': 70, 'velocity': 100}]
            [{'note': 90, 'velocity': 100}]
            [{'note': 60, 'velocity': 100}]

        If it is a polyphonic pattern, i.e. a dictionary where one or more
        of the values indexed by the above algorithm are also lists, the
        elements of each list are paired together into several reduced patterns.
        The number of messages is determined by the length of the longest list.
        Any lists that are shorter than the longest list will repeat its
        elements from the start to match the length of the longest list.
        Any values that are not lists are simply repeated.

        When `use_divisor_to_skip` is True and the `divisor` is a number
        other than 1, patterns are only generated if the iterator is
        divisible by the divisor, and will otherwise yield zero messages.
        """

        # TODO: more examples for pattern_reduce()
        # TODO: document pattern_reduce() arguments
        def maybe_parse(val: ParsableElement) -> RecursiveElement:
            if isinstance(val, str):
                return self.env.parser.parse(val)
            if isinstance(val, list) and all(isinstance(item, str) for item in val):
                val = " ".join(val)
                return self.env.parser.parse(val)
            return val

        if any(isinstance(n, (list, str)) for n in (divisor, rate)):
            divisor, rate = next(
                self.pattern_reduce({"divisor": divisor, "rate": rate}, iterator)
            ).values()

        if use_divisor_to_skip and iterator % divisor != 0:
            return

        pattern = {k: maybe_parse(v) for k, v in pattern.items()}

        for k, v in pattern.items():
            pattern[k] = self.pattern_element(v, iterator, divisor, rate)

        if not any(isinstance(v, list) for v in pattern.values()):
            # Base case where we have a monophonic message
            yield pattern

        # For polyphonic messages, recursively reduce them
        # to a list of monophonic messages
        max_length = max(_maybe_length(v) for v in pattern.values())
        for i in range(max_length):
            sub_pattern = {k: _maybe_index(v, i) for k, v in pattern.items()}
            yield from self.pattern_reduce(sub_pattern, iterator, divisor, rate)

    def cycle_loaf(self, loaf: Optional[int], on: Optional[tuple | int]) -> bool:
        """
        Will slice time in group of bars of size "loaf". Will
        check if the current bar matches with one of the selected
        bars in the sliced group (e.g. for a slice of 5, select
        when we are on bar 1 and 3).
        """

        def mod_cycles(on: int | tuple) -> bool:
            """
            Modulo operator working on bar numbers. This function will
            be used with the "on" operator if no "loaf" argument is used
            by the pattern.
            """

            on = on[0] if isinstance(on, tuple) else on
            return self.env.clock.bar % on == 0

        if loaf is None and on is None:
            return True

        if loaf is None:
            return mod_cycles(on=on)

        measure = self.env.clock.bar
        elapsed_bars = measure // loaf
        bar_in_current_group = measure - (elapsed_bars * loaf)

        if isinstance(on, tuple):
            return bar_in_current_group in tuple(x - 1 for x in on)

        return bar_in_current_group == (on - 1)

    def euclid_bars(
        self,
        steps: int,
        pulses: int,
        rotation: Optional[int] = None,
        negative: bool = False,
    ):
        """
        Euclidian rhythm but on the measure level!
        """
        if rotation is None:
            rotation = 0
        euclidian_pattern = euclid(steps, pulses, rotation)
        if negative:
            euclidian_pattern = list(map(lambda x: x ^ 1, euclidian_pattern))
        to_bars, len_in_bars = [], len(euclidian_pattern)

        for count, value in enumerate(euclidian_pattern):
            if value == 1:
                to_bars.append(count + 1)

        return self.cycle_loaf(loaf=len_in_bars, on=tuple(to_bars))

    def binary_bars(self, binary_pattern: list):
        """
        Euclidian rhythm but on the measure level!
        """
        # We can't tolerate any other thing than 1 and 0
        if not all(e in [1, 0] for e in binary_pattern):
            return False

        to_bars, len_in_bars = [], len(binary_pattern)

        for count, value in enumerate(binary_pattern):
            if value == 1:
                to_bars.append(count + 1)

        return self.cycle_loaf(loaf=len_in_bars, on=tuple(to_bars))

    def chance_operation(self, frequency: str):
        """
        Port of the TidalCycles sometimes family of functions:
        - always: 100%
        - almostAlways: 90%
        - often: 75%
        - sometimes: 50%
        - rarely: 25%
        - AlmostNever: 10%
        - never: 0%

        These functions represent a likelihood for an event to be played.
        """
        chance = {
            "always": True,
            "almostAlways": random() <= 0.90,
            "often": random() <= 0.75,
            "sometimes": random() <= 0.5,
            "rarely": random() <= 0.25,
            "almostNever": random() <= 0.10,
            "never": False,
        }
        return chance.get(frequency, False)

    def key_deleter(self, dictionary: dict, list_of_keys: list[str]):
        """
        Remove multiple keys from one dictionary in one-go
        while taking care of possible index errors.
        """
        for key in list_of_keys:
            try:
                del dictionary[key]
            except KeyError:
                pass

    def apply_conditional_mask_to_bars(self, pattern: ParsableElement) -> bool:
        boolean_masks = []

        # Cycle loaf
        boolean_masks.append(
            self.cycle_loaf(loaf=pattern.get("loaf", None), on=pattern.get("on", None))
        )

        # Euclidian
        if (
            pattern.get("euclid", None) is not None
            or pattern.get("eu", None) is not None
        ):
            steps, pulses = pattern.get("euclid")[0:2]
            try:
                rotation = pattern["euclid"][2]
            except IndexError:
                rotation = None
            boolean_masks.append(self.euclid_bars(steps, pulses, rotation))

        # Negative euclidian
        if (
            pattern.get("neuclid", None) is not None
            or pattern.get("neu", None) is not None
        ):
            steps, pulses = pattern.get("neuclid")[0:2]
            try:
                rotation = pattern["neuclid"][2]
            except IndexError:
                rotation = None
            boolean_masks.append(
                self.euclid_bars(steps, pulses, rotation, negative=True)
            )

        # Binary pattern
        if pattern.get("binary", None) is not None:
            boolean_masks.append(self.binary_bars(binary_pattern=pattern["binary"]))

        # Chance operation
        if pattern.get("chance", None) is not None:
            boolean_masks.append(self.chance_operation(frequency=pattern["chance"]))

        # Cleaning up the messy keys
        self.key_deleter(
            dictionary=pattern,
            list_of_keys=["euclid", "neuclid", "on", "loaf", "binary" "chance"],
        )

        # Returning if one False in the boolean masks
        return False in boolean_masks
