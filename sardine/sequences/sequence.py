import itertools
import random
from typing import Union


def bin(sequence: Union[str, Union[int, float]], reverse: bool = False):
    """
    Binary sequence: transform a string of 1 and 0 to a list
    of boolean values to be used by the `trig` parameter key.
    Also works with integers. Will turn an integer into its
    binary representation.
    """
    if isinstance(sequence, str):
        binary = []
        for char in sequence.replace(" ", ""):
            binary.append(1) if char == "1" else binary.append(0)
        if reverse:
            binary.reverse()
        return binary
    elif isinstance(sequence, (int, float)):
        binary = list(format(sequence, "b"))
        if reverse:
            binary.reverse()
        return binary


def text_eater(sequence: str, reverse: bool = False):
    """
    Given a string input, will output an ASCII number for each letter in the
    corresponding text. Non ASCII characters will be discarded.
    """

    def remove_non_ascii(string):
        return "".join(char for char in string if ord(char) < 128)

    text_to_ascii = [ord(c) for c in remove_non_ascii(sequence)]
    if reverse:
        text_to_ascii.reverse()
    return text_to_ascii


def xox(sequence: str, reverse: bool = False):
    """Simple beat sequencer function"""
    fseq = []
    for char in sequence:
        if char == "x":
            fseq.append(1)
        elif char == "?":
            fseq.append(1 if random.random() > 0.5 else 0)
        elif char == " ":
            fseq.append(0)
        else:
            raise RuntimeError('Characters are limited to "x", " " and "?".')
    if reverse:
        fseq.reverse()
    return itertools.cycle(fseq)


# Found here: https://github.com/tsmorrill/Sweepings/blob/main/python3/euclid_descent.py
# Paper: https://arxiv.org/pdf/2206.12421.pdf



def _starts_descent(list, index):
    length = len(list)
    next_index = (index + 1) % length
    return list[index] > list[next_index]


def euclidian_rhythm(pulses: int, length: int, rotate: int = 0):
    """Calculate Euclidean rhythms"""
    if pulses >= length:
        return [1]
    res_list = [pulses * t % length for t in range(-1, length - 1)]
    bool_list = [_starts_descent(res_list, index) for index in range(length)]

    def rotation(l, n):
        return l[-n:] + l[:-n]

    return rotation([1 if x is True else 0 for x in bool_list], rotate)


euclid = euclidian_rhythm


def E(step: int, maximum: int, index: int) -> bool:
    """Euclidian rhythms at the Python level"""
    pattern = euclid(step, maximum)
    return True if pattern[index % len(pattern)] == 1 else False


def mod(mod: int, i: int) -> bool:
    """Modulo using iterators"""
    return True if i % mod == 0 else False


def imod(mod: int, i: int) -> bool:
    """Inverse of the modulo using iterators"""
    return True if i % mod == 0 else False


def pick(*args) -> list:
    """Alternative function to use random.choice. More terse"""
    return random.choice(list(args))
