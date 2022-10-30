import random
from .Utilities import zip_cycle, map_unary_function, map_binary_function
from itertools import cycle
from math import cos, sin, tan


def expand(collection):
    """Chance-based operation. Apply a random octave transposition process
    to every note in a given collection.

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: Chance-expanded list of integers
    """

    def expand_number(number):
        expansions = [0, -12, 12]
        return number + random.choice(expansions)

    return map_unary_function(expand_number, collection)


def disco(collection):
    """Takes every other note down an octave

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: A list of integers
    """
    if not isinstance(collection, list):
        return collection
    else:
        offsets = cycle([-12, 0])
        return [x + offset for (x, offset) in zip(collection, offsets)]


def palindrome(collection):
    """Make a palindrome out of a newly generated collection

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: palindromed list of integers from qualifier's based
        collection
    """
    if not isinstance(collection, list):
        return collection
    else:
        return collection + list(reversed(collection))


def reverse(collection):
    """Reverse a newly generated collection.

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: reversed list of integers from qualifier's based collection
    """
    if not isinstance(collection, list):
        return collection
    else:
        return reversed(collection)


def braid(collection):
    """Take the first half of a list, take its second half, interleave.

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: An interleaved list of integers
    """
    if not isinstance(collection, list):
        return collection
    else:
        col_len = len(collection) // 2
        first, second = collection[:col_len], collection[col_len:]
        return [val for pair in zip(first, second) for val in pair]


def shuffle(collection):
    """Shuffle a newly generated collection

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: A shuffled list of integers
    """
    if not isinstance(collection, list):
        return collection
    else:
        random.shuffle(collection)
        return collection


def drop2(collection):
    """Simulate a drop2 chord.

    Args:
        collection (list): A list of integers

    Returns:
        list: A list of integers with the second note dropped an octave.
    """
    if not isinstance(collection, list):
        return collection
    else:
        collection[1] = collection[1] - 12
        return collection


def drop3(collection):
    """Simulate a drop3 chord.

    Args:
        collection (list): A list of integers

    Returns:
        list: A list of integers with the third note dropped an octave.
    """
    if not isinstance(collection, list):
        return collection
    else:
        collection[2] = collection[2] - 12
        return collection


def drop2and4(collection):
    """Simulate a drop2&4 chord.

    Args:
        collection (list): A list of integers

    Returns:
        list: A list of integers with the second and fourth note dropped
        an octave.
    """
    if not isinstance(collection, list):
        return collection
    else:
        collection[1] = collection[1] - 12
        collection[3] = collection[3] - 12
        return collection


def cosinus(self, x):
    return map_unary_function(cos, x)


def sinus(self, x):
    return map_unary_function(sin, x)


def tangente(self, x):
    return map_unary_function(tan, x)
