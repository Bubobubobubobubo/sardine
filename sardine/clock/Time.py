class Time:
    def __init__(
        self, phase: float=0.0, beat: float=0.0, bar: int=0,
        beats_per_bar: int = 4
    ):
        self._phase, self._beat, self._bar = phase, beat, bar
        self._beats_per_bar = 4

    @property
    def phase(self) -> float:
        return self._phase

    @phase.setter
    def phase(self, phase: float) -> None:
        self._phase = float(phase)

    @property
    def beat(self) -> float:
        return self._beat

    @beat.setter
    def phase(self, beat: float) -> None:
        self._beat = float(beat)

    @property
    def bar(self) -> int:
        return self._bar

    @bar.setter
    def bar(self, bar: int) -> None:
        self._bar = float(bar)


