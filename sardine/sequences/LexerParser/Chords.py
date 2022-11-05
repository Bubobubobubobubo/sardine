class Chord():
    """
    Chord is a polyphonic token. It will be sent out
    as a polyphonic object when trated by the `.out()`
    method.
    """
    def __init__(self, elements: list):
        self._elements = elements

    @property
    def elements(self):
        return self._elements

    def __repr__(self) -> str:
        return f"Chord: ({self._elements})"

    def __str__(self) -> str:
        return f"Chord: ({self._elements})"
