from random import choices as randomChoices
from random import randint, random

# ==============================================================================#

# Inspired by TidalCycles
def always():
    return True


def almostAlways():
    return True if random() < 0.90 else False


def often():
    return True if random() < 0.75 else False


def sometimes():
    return True if random() < 0.5 else False


def rarely():
    return True if random() < 0.25 else False


def almostNever():
    return True if random() < 0.10 else False


def never():
    return False


def dice(number):
    return randint(1, 6) == number


def d4(number):
    return randint(1, 4) == number


def d6(number):
    return randint(1, 6) == number


def d8(number):
    return randint(1, 8) == number


def d12(number):
    return randint(1, 12) == number


def d20(number):
    return randint(1, 20) == number


def pick(*args):
    return randomChoices(list(args)).pop()
