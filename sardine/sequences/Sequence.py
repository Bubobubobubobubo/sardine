from typing import Union
import itertools
import random


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


def euclidean_rhythm(beats: int, pulses: int, rotation: int = 0, lo: int = 0, hi: int = 1):
    """Computes Euclidean rhythm of beats/pulses
    Examples:
        euclidean_rhythm(8, 5)          -> [1, 0, 1, 1, 0, 1, 1, 0]
        euclidean_rhythm(8, 5, 1, 0, 1) -> [0, 1, 1, 0, 1, 1, 0, 1]
        euclidean_rhythm(8, 5, 1, 1, 2) -> [1, 2, 2, 1, 2, 2, 1, 2]
    Args:
        beats  (int): Beats of the rhythm
        pulses (int): Pulses to distribute. Should be <= beats
        rotation (int): Number of beats to shift on result i.e. [0,1,2] => [1,2,0]
        lo (int): low value (rest)
        hi (int): high value (pulse)
    Returns:
        list: An unidimensional list of integers (#hi and #lo values) with #beats length and #pulses number of #hi values
    Inspired by:
        - https://kountanis.com/2017/06/13/python-euclidean/
        - [Foxdot](https://github.com/Qirky/FoxDot/blob/76318f9630bede48ff3994146ed644affa27bfa4/FoxDot/lib/Utils/__init__.py#L69)
    """
    beats, pulses, rotation, hi, lo = int(beats), int(pulses), int(rotation), int(hi), int(lo)

    if pulses == 0: return [pulses for i in range(beats)]

    # Initialization of the lookup as a 2-dimension list containing a #pulses
    # number of hi values and a (#beats - #pulses) number of lo values
    # eg: [[1], [1], [1], [1], [1], [0], [0], [0]]
    lookup = [[hi if i < pulses else lo] for i in range(beats)]

    while True:
        beats = beats - pulses
        if beats <= 1:
            break
        elif beats < pulses:
            pulses, beats = beats, pulses
        for i in range(pulses):
            # The last element of the lookup list is appended to its #i element
            # and then removed
            # e.g. [[1], [1], [1], [1], [1], [0], [0], [0]]
            # =>   [[1, 0], [1], [1], [1], [1], [0], [0]]
            lookup[i] += lookup[-1]
            del lookup[-1]

    # The lookup list needs to be flattened
    # [[1, 0, 1], [1, 0, 1], [1, 0]] => [1, 0, 1, 1, 0, 1, 1, 0]
    result = [x for y in lookup for x in y]

    if rotate != 0:
        result = result[rotation:] + result[:rotation]

    return result


euclid = euclidean_rhythm


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
    return choice(list(args))
