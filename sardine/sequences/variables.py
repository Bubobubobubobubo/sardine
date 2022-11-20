from itertools import count
from string import ascii_letters
from typing import Union

__all__ = ("Variables",)


class Variables(object):
    def __init__(self):
        """
        Variables are named after the letters of the alphabet. They simply are
        variables object wrapped in a different way so that they can be used
        more easily live.
        """
        self._iterators = {}
        for c in ascii_letters:
            self._iterators[c] = 0

    def reset(self, iterator: Union[str, None] = None):
        if not iterator:
            self._iterators = {}
            for c in ascii_letters:
                self._iterators[c] = 0
        else:
            self._iterators[iterator] = 0

    def __getattribute__(self, name):
        """Overriden attribute getter"""
        if name in ascii_letters:
            return self._iterators[name]
        return super(Variables, self).__getattribute__(name)

    def __setattr__(self, name, value):
        """
        Overriden attribute setter.

        You can provide an integer (eg. 1, 123) or a two-number list of
        integers ([1,5], [10,100]). The first number is the base value,
        the second number is the step increment.
        """
        if name in ascii_letters:
            if isinstance(value, (int, float, str, list)):
                self._iterators[name] = value
            else:
                raise ValueError("You can only set int, floats, list or strings")
        else:
            super(Variables, self).__setattr__(name, value)
