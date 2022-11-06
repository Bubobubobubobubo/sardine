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

    def __len__(self) -> int:
        return len(self._elements)

    def __getitem__(self, key):
        """Used for composing polyphonic messages"""
        return self._elements[key % len(self._elements) - 1]

    def _clamp(self) -> list:
        def _clamp(n, smallest, largest): 
            return max(smallest, min(n, largest))
        return list(map(lambda x: _clamp(x, 0, 127), self._elements))
