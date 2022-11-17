class Time:
    def __init__(
        self,
        origin: float = 0.0,
    ):
        self.origin = origin

    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            " ".join(
                f"{attr}={getattr(self, attr)}"
                for attr in ("origin",)
            ),
        )

    def reset(self):
        """Resets the time origin back to 0."""
        self.origin = 0.0
