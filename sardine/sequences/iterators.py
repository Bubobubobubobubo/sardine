from itertools import count
from string import ascii_letters
from typing import Union

__all__ = ("Iterator",)


class Iterator(object):
    def __init__(self):
        """
        Iterators are named after the letters of the alphabet. They simply are the
        itertools.count object wrapped in a different way so that they can be used
        more easily live. You can easily specify the step count by setting the res-
        pective attribute using a list of two numbers (eg. [0, 5] for a 5 by 5 step
        increment.
        """
        self._iterators = {}
        for c in ascii_letters:
            self._iterators[c] = count(0)

    def reset(self, iterator: Union[str, None] = None):
        if not iterator:
            self._iterators = {}
            for c in ascii_letters:
                self._iterators[c] = count(0)
        else:
            self._iterators[iterator] = count(0)

    def __getattribute__(self, name):
        """Overriden attribute getter"""
        if name in ascii_letters:
            return next(self._iterators[name])
        return super(Iterator, self).__getattribute__(name)

    def __setattr__(self, name, value):
        """
        Overriden attribute setter.

        You can provide an integer (eg. 1, 123) or a two-number list of
        integers ([1,5], [10,100]). The first number is the base value,
        the second number is the step increment.
        """
        if name in ascii_letters:
            if isinstance(value, int):
                self._iterators[name] = count(value)
            elif isinstance(value, list) and len(value) == 2:
                # This is for the step value
                self._iterators[name] = count(value[0], value[1])
        else:
            super(Iterator, self).__setattr__(name, value)
