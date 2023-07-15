import operator
from fractions import Fraction
from functools import partial, reduce, wraps


def flatten(lst) -> list:
    """Flattens a list of lists"""
    return [item for sublist in lst for item in sublist]


def remove_nones(lst) -> list:
    """Removes 'None' values from given list"""
    return filter(lambda x: x != None, lst)


def id(x):
    """Identity function"""
    return x


def merge_dicts(a, b, op=operator.add):
    return dict(a.items() + b.items() + [(k, op(a[k], b[k])) for k in set(b) & set(a)])


def rotate_left(lst, n):
    """Rotate an array `n` elements to the left"""
    return lst[n:] + lst[:n]


def partial_function(f):
    """Decorator for functions to support partial application. When not given enough
    arguments, a decoracted function will return a new function for the remaining
    arguments"""

    def wrapper(*args):
        try:
            return f(*args)
        except TypeError as e:
            return partial(f, *args)

    return wrapper


def show_fraction(frac):
    if frac == None:
        return "None"

    if frac.denominator == 1:
        return str(frac.numerator)

    lookup = {
        Fraction(1, 2): "½",
        Fraction(1, 3): "⅓",
        Fraction(2, 3): "⅔",
        Fraction(1, 4): "¼",
        Fraction(3, 4): "¾",
        Fraction(1, 5): "⅕",
        Fraction(2, 5): "⅖",
        Fraction(3, 5): "⅗",
        Fraction(4, 5): "⅘",
        Fraction(1, 6): "⅙",
        Fraction(5, 6): "⅚",
        Fraction(1, 7): "⅐",
        Fraction(1, 8): "⅛",
        Fraction(3, 8): "⅜",
        Fraction(5, 8): "⅝",
        Fraction(7, 8): "⅞",
        Fraction(1, 9): "⅑",
        Fraction(1, 10): "⅒",
    }
    if frac in lookup:
        result = lookup[frac]
    else:
        result = "(%d/%d)" % (frac.numerator, frac.denominator)
    return result


def curry(f):
    @wraps(f)
    def _(arg):
        try:
            return f(arg)
        except TypeError:
            return curry(wraps(f)(partial(f, arg)))

    return _


def uncurry(f):
    @wraps(f)
    def _(*args):
        return reduce(lambda x, y: x(y), args, f)

    return _
