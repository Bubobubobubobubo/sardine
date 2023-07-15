class Chord(list):
    """
    Chord is a polyphonic token. It will be sent out
    as a polyphonic object when trated by the `.out()`
    method.
    """

    def __init__(self, *args):
        super().__init__(item for item in args)

    def __repr__(self) -> str:
        return f"Chord: ({list(self)})"

    def __str__(self) -> str:
        return f"Chord: ({list(self)})"

    def __mul__(self, other):
        if isinstance(other, list):
            return [self * x for x in other]
        return Chord(*[x * other for x in self])

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, list):
            return [self / x for x in other]
        return Chord(*[x / other for x in self])

    def __rtruediv__(self, other):
        return self / other

    def __add__(self, other):
        if isinstance(other, list):
            return [self + x for x in other]
        return Chord(*[x + other for x in self])

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, list):
            return [self - x for x in other]
        return Chord(*[x - other for x in self])

    def __rsub__(self, other):
        return self - other

    def __setitem__(self, index, item):
        super().__setitem__(index, item)

    def _clamp(self) -> list:
        """Clamp all values to range 0-127 for MIDI Notes"""

        def _clamp(n, smallest, largest):
            return max(smallest, min(n, largest))

        return Chord(*map(lambda x: _clamp(x, 0, 127), self))
