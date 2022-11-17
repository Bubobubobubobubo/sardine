import contextlib
import contextvars

shift = contextvars.ContextVar("shift", default=0.0)
"""
This specifies the amount of time to offset in the current context.
Usually this is updated within the context of scheduled functions
to simulate sleeping without actually blocking the function. Behavior is
undefined if time is shifted in the global context.
"""


class Time:
    """Contains the origin of a FishBowl's time.

    Any new clocks must continue from this origin when they are running,
    and must update the origin when they are paused or stopped.
    """
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

    @property
    def shift(self) -> float:
        """The time shift in the current context.

        This is useful for simulating sleeps without blocking.
        """
        return shift.get()

    @shift.setter
    def shift(self, seconds: int):
        shift.set(seconds)

    @contextlib.contextmanager
    def scoped_shift(self, seconds: float):
        """Returns a context manager that adds `seconds` to the clock.

        After the context manager is exited, the time shift is restored
        to its previous value.
        """
        token = shift.set(shift.get() + seconds)
        try:
            yield
        finally:
            shift.reset(token)
