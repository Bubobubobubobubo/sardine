from .Messages import *


def plural(n: int, word: str, suffix: str = "s"):
    return word if n == 1 else word + suffix
