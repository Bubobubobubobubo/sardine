import itertools
import random


def bin(sequence: str, reverse: bool = False):
    """
    Binary sequence: transform a string of 1 and 0 to a list
    of boolean values to be used by the `trig` parameter key.
    """
    binary = []
    for char in sequence.replace(" ", ""):
        binary.append(True) if char == "1" else binary.append(False)

    if reverse:
        binary.reverse()

    return itertools.cycle(binary)


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


def euclidean_rhythm(beats: int, pulses: int, rotation: int = 0):
    """Computes Euclidean rhythm of beats/pulses

    Examples:
        euclidean_rhythm(8, 5) -> [1, 0, 1, 0, 1, 0, 1, 1]
        euclidean_rhythm(7, 3) -> [1, 0, 0, 1, 0, 1, 0]

    Args:
        beats  (int): Beats of the rhythm
        pulses (int): Pulses to distribute. Should be <= beats

    Returns:
        list: 1s are pulses, zeros rests

    Taken from: https://kountanis.com/2017/06/13/python-euclidean/
    """

    def rotate(seq, k):
        return seq[k:] + seq[:k]

    if pulses is None or pulses < 0:
        pulses = 0
    if beats is None or beats < 0:
        beats = 0
    if pulses > beats:
        beats, pulses = pulses, beats
    if beats == 0:
        return []

    rests = beats - pulses
    result = [1] * pulses
    pivot = 1
    interval = 2

    while rests > 0:
        if pivot > len(result):
            pivot = 1
            interval += 1

        result.insert(pivot, 0)

        pivot += interval
        rests -= 1

    if rotate != 0:
        result = rotate(result, rotation)

    return itertools.cycle(result)


euclid = euclidean_rhythm
