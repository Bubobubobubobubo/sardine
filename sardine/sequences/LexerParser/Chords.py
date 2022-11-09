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

    def __setitem__(self, index, item):
        super().__setitem__(index, item)

    def _clamp(self) -> list:
        """Clamp all values to range 0-127 for MIDI Notes"""

        def _clamp(n, smallest, largest):
            return max(smallest, min(n, largest))

        return Chord(*map(lambda x: _clamp(x, 0, 127), self))
