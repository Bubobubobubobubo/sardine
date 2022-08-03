import itertools


def bin(sequence: str):
    """
    Binary sequence: transform a string of 1 and 0 to a list
    of boolean values to be used by the `trig` parameter key.
    """
    binary = []
    for char in sequence.replace(' ', ''):
        binary.append(True) if char=="1" else binary.append(False)
    return itertools.cycle(binary)


def bjorklund(steps, pulses):
    """
    Bjorklund alorithm used for the generation of euclidian
    rhythms. Stolen from a GitHub repository :
    https://github.com/brianhouse/bjorklund/blob/master/__init__.py

    Note: this algorithm doesn't support rotation but it could
    be added later.
    """
    steps = int(steps)
    pulses = int(pulses)
    if pulses > steps:
        raise ValueError
    pattern = []
    counts = []
    remainders = []
    divisor = steps - pulses
    remainders.append(pulses)
    level = 0
    while True:
        counts.append(divisor // remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level = level + 1
        if remainders[level] <= 1:
            break
    counts.append(divisor)

    def build(level):
        if level == -1:
            pattern.append(0)
        elif level == -2:
            pattern.append(1)
        else:
            for i in range(0, counts[level]):
                build(level - 1)
            if remainders[level] != 0:
                build(level - 2)

    build(level)
    i = pattern.index(1)
    pattern = pattern[i:] + pattern[0:i]
    return pattern
