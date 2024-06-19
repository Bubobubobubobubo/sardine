from random import choice, randint, random

never = lambda: False
almostNever = lambda: random() < 0.10
rarely = lambda: random() < 0.25
sometimes = lambda: random() > 0.5
often = lambda: random() > 0.75
almostAlways = lambda: random() > 0.90
always = lambda: True
dice = lambda x: randint(0, 6) in x


########################################################################################
# EUCLIDIAN RHYTHM IMPLEMENTATION
# Found here: https://github.com/tsmorrill/Sweepings/blob/main/python3/euclid_descent.py
# Paper: https://arxiv.org/pdf/2206.12421.pdf
########################################################################################


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
    return choice(list(args))
