from functools import wraps
from typing import Union
from ..sequences import Chord
from math import floor

VALUES = Union[int, float, list, str]
PATTERN = dict[str, list[float | int | list | str]]
REDUCED_PATTERN = dict[str, list[float | int]]

@staticmethod
def _alias_param(name, alias):
    """
    Alias a keyword parameter in a function. Throws a TypeError when a value is
    given for both the original kwarg and the alias. Method taken from
    github.com/thegamecracks/abattlemetrics/blob/main/abattlemetrics/client.py
    (@thegamecracks).
    """
    MISSING = object()

    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            alias_value = kwargs.pop(alias, MISSING)
            if alias_value is not MISSING:
                if name in kwargs:
                    raise TypeError(f'Cannot pass both {name!r} and {alias!r} in call')
                kwargs[name] = alias_value
            return func(*args, **kwargs)
        return wrapper
    return deco


class Sender:

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

    def pattern_element(self, div: int, rate: int, iterator: int, pattern: list) -> int:
        """Joseph Enguehard's algorithm for solving iteration speed"""
        return floor(iterator * rate / div) % len(pattern)

    def pattern_reduce(self,
            pattern: PATTERN,
            iterator: int,
            divisor: int,
            rate: float,
    ) -> dict:
        pattern = {
                k: self.env.parser.parse(v) if isinstance(
            v, str) else v for k, v in pattern.items()
        }
        pattern = {
                k:v[self.pattern_element(
                    div=divisor,
                    rate=rate,
                    iterator=iterator,
                    pattern=v)] if hasattr(
                        v, "__getitem__") else v for k, v in pattern.items()
        }
        return pattern


    def reduce_polyphonic_message(
            self,
            pattern: PATTERN) -> list[dict]:
        """
        Reduce a polyphonic message to a list of messages represented as
        dictionaries holding values to be sent through the MIDI Port
        """
        message_list: list = []
        length = [x for x in filter(
            lambda x: hasattr(x, '__getitem__'), pattern.values())
        ]
        length = max([len(i) for i in length])

        # Break the chords into lists
        pattern = {k:list(value) if isinstance(
            value, Chord) else value for k, value in pattern.items()}

        for _ in range(length):
            message_list.append({k:v[_%len(v)] if isinstance(
                v, (Chord, list)) else v for k, v in pattern.items()}
            )
        return message_list

