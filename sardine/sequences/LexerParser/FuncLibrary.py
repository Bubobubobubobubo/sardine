import random
from .Utilities import zip_cycle, map_unary_function, map_binary_function
from itertools import cycle
from math import cos, sin, tan
from typing import Union


def expand(collection):
    """Chance-based operation. Apply a random octave transposition process
    to every note in a given collection.

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: Chance-expanded list of integers
    """

    def expand_number(number: Union[int, float]) -> Union[int, float]:
        expansions = [0, -12, 12]
        return number + random.choice(expansions)

    return map_unary_function(expand_number, collection)


def disco(collection: list) -> list:
    """Takes every other note down an octave

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: A list of integers
    """
    offsets = cycle([0, -12])
    return [x + offset for (x, offset) in zip(collection, offsets)]


def palindrome(collection: list) -> list:
    """Make a palindrome out of a newly generated collection

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: palindromed list of integers from qualifier's based
        collection
    """
    return collection + list(reversed(collection))


def reverse(collection: list) -> list:
    """Reverse a newly generated collection.

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: reversed list of integers from qualifier's based collection
    """
    return list(reversed(collection))


def braid(collection: list) -> list:
    """Take the first half of a list, take its second half, interleave.

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: An interleaved list of integers
    """
    col_len = len(collection) // 2
    first, second = collection[:col_len], collection[col_len:]
    return [val for pair in zip(first, second) for val in pair]


def shuffle(collection: list) -> list:
    """Shuffle a newly generated collection

    Args:
        collection (list): A list generated through a qualifier

    Returns:
        list: A shuffled list of integers
    """
    random.shuffle(collection)
    return collection


def drop2(collection: list) -> list:
    """Simulate a drop2 chord.

    Args:
        collection (list): A list of integers

    Returns:
        list: A list of integers with the second note dropped an octave.
    """
    collection[1] = collection[1] - 12
    return collection


def drop3(collection: list) -> list:
    """Simulate a drop3 chord.

    Args:
        collection (list): A list of integers

    Returns:
        list: A list of integers with the third note dropped an octave.
    """
    collection[2] = collection[2] - 12
    return collection


def drop2and4(collection: list) -> list:
    """Simulate a drop2&4 chord.

    Args:
        collection (list): A list of integers

    Returns:
        list: A list of integers with the second and fourth note dropped
        an octave.
    """
    collection[1] = collection[1] - 12
    collection[3] = collection[3] - 12
    return collection


def cosinus(x: list) -> list:
    """Basic cosinus function

    Args:
        x (list): pattern

    Returns:
        list: a valid pattern.
    """
    return map_unary_function(cos, x)


def sinus(x: list) -> list:
    """Basic sinus function

    Args:
        x (list): pattern

    Returns:
        list: a valid pattern.
    """
    return map_unary_function(sin, x)


def tangent(x: list) -> list:
    """Basic tangent function

    Args:
        x (list): pattern

    Returns:
        list: a valid pattern.
    """
    return map_unary_function(tan, x)

# Qualifiers List

qualifiers = {
    "dim": [0, 3, 6, 12],
    "dim9": [0, 3, 6, 9, 14],
    "hdim7": [0, 3, 6, 10],
    "hdim9": [0, 3, 6, 10, 14],
    "hdimb9": [0, 3, 6, 10, 13],
    "dim7": [0, 3, 6, 9],
    "7dim5": [0, 4, 6, 10],
    "aug": [0, 4, 8, 12],
    "augMaj7": [0, 4, 8, 11],
    "aug7": [0, 4, 8, 10],
    "aug9": [0, 4, 10, 14],
    "maj": [0, 4, 7, 12],
    "maj7": [0, 4, 7, 11],
    "maj9": [0, 4, 11, 14],
    "minmaj7": [0, 3, 7, 11],
    "5": [0, 7, 12],
    "6": [0, 4, 7, 9],
    "7": [0, 4, 7, 10],
    "9": [0, 4, 10, 14],
    "b9": [0, 4, 10, 13],
    "mM9": [0, 3, 11, 14],
    "min": [0, 3, 7, 12],
    "min7": [0, 3, 7, 10],
    "min9": [0, 3, 10, 14],
    "sus4": [0, 5, 7, 12],
    "sus2": [0, 2, 7, 12],
    "b5": [0, 4, 6, 12],
    "mb5": [0, 3, 6, 12],
    # Scales begin here
    # Based on a very partial list found here:
    # https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "hminor": [0, 2, 3, 5, 7, 8, 11],
    "^minor": [0, 2, 3, 5, 7, 9, 11],  # doesn't work
    "vminor": [0, 2, 3, 5, 7, 8, 10],
    "penta": [0, 2, 4, 7, 9],
    "acoustic": [0, 2, 4, 6, 7, 9, 10],
    "aeolian": [0, 2, 3, 5, 7, 8, 10],
    "algerian": [0, 2, 3, 6, 7, 9, 11, 12, 14, 15, 17],
    "superlocrian": [0, 1, 3, 4, 6, 8, 10],
    "augmented": [0, 3, 4, 7, 8, 11],
    "bebop": [0, 2, 4, 5, 7, 9, 10, 11],
    "blues": [0, 3, 5, 6, 7, 10],
    "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "doubleharmonic": [0, 1, 4, 5, 8, 11],
    "enigmatic": [0, 1, 4, 6, 8, 10, 11],
    "flamenco": [0, 1, 4, 5, 7, 8, 11],
    "gypsy": [0, 2, 3, 6, 7, 8, 10],
    "halfdim": [0, 2, 3, 5, 6, 8, 10],
    "harmmajor": [0, 2, 4, 5, 7, 8, 11],
    "harmminor": [0, 2, 3, 5, 7, 8, 11],
    "hirajoshi": [0, 4, 6, 7, 11],
    "hungarianminor": [0, 2, 3, 6, 7, 8, 11],
    "hungarianmajor": [0, 3, 4, 6, 7, 9, 10],
    "in": [0, 1, 5, 7, 8],
    "insen": [0, 1, 5, 7, 10],
    "ionian": [0, 2, 4, 5, 7, 9, 11],
    "istrian": [0, 1, 3, 4, 6, 7],
    "iwato": [0, 1, 5, 6, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10],
    "lydianaug": [0, 2, 4, 6, 8, 9, 11],
    "lydian": [0, 2, 4, 5, 7, 8, 9, 11],
    "majorlocrian": [0, 2, 4, 5, 6, 8, 10],
    "majorpenta": [0, 2, 4, 7, 9],
    "minorpenta": [0, 3, 5, 7, 10],
    "melominup": [0, 2, 3, 5, 7, 9, 11],
    "melomindown": [0, 2, 3, 5, 7, 8, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "neapolitan": [0, 1, 3, 5, 7, 8, 11],
    "octatonic": [0, 2, 3, 5, 6, 8, 9, 11],
    "octatonic2": [0, 1, 3, 4, 6, 7, 9, 10],
    "persian": [0, 1, 4, 5, 6, 8, 11],
    "phrygian": [0, 1, 4, 5, 7, 8, 10],
    "prometheus": [0, 2, 4, 6, 9, 10],
    "harmonics": [0, 3, 4, 5, 7, 9],
    "tritone": [0, 1, 4, 6, 7, 10],
    "ukrainian": [0, 2, 3, 6, 7, 9, 10],
    "whole": [0, 2, 4, 6, 8, 10],
    "yo": [0, 3, 5, 7, 10],
    "symetrical": [0, 1, 2, 6, 7, 10],
    "symetrical2": [0, 2, 3, 6, 8, 10],
    "messiaen1": [0, 2, 4, 6, 8, 10],
    "messiaen2": [0, 1, 3, 4, 6, 7, 9, 10],
    "messiaen3": [0, 2, 3, 4, 6, 7, 8, 10, 11],
    "messiaen4": [0, 1, 2, 4, 6, 7, 8, 11],
    "messiaen5": [0, 1, 5, 6, 7, 11],
    "messiaen6": [0, 2, 4, 5, 6, 8],
    "messiaen7": [0, 1, 2, 3, 5, 6, 7, 8, 9, 11],
    # Structures (other musical objects)
    "fourths": [0, 4, 10, 15, 20],
    "fifths": [0, 7, 14, 21, 28],
    "sixths": [0, 9, 17, 26, 35],
    "thirds": [0, 4, 8, 12],
    "octaves": [0, 12, 24, 36, 48],
}
