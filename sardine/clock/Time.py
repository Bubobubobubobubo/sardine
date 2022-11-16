import contextlib
import contextvars

time_shift = contextvars.ContextVar("time_shift", default=0.0)
"""
This specifies the amount of time to offset in the current context.
Usually this is updated within the context of scheduled functions
to simulate sleeping without actually blocking the function. Behavior is
undefined if time is shifted in the global context.
"""

class Time:
    def __init__(
        self,
        elapsed_time: float=0.0,
    ):
        self._elapsed_time = elapsed_time

    def __repr__(self) -> str:
        return f"Started: {self._elapsed_time} seconds ago."

    def reset(self):
        """Reset elasped time"""
        self._elapsed_time = 0.0

    @property
    def elapsed_time(self) -> float:
        """The amount of time elapsed including the current time shift."""
        return self._elapsed_time + self.time_shift

    @property
    def time_shift(self) -> float:
        """The time shift in the current context.

        This is useful for simulating sleeps without blocking.
        """
        return time_shift.get()

    @time_shift.setter
    def time_shift(self, n_ticks: int):
        time_shift.set(n_ticks)

    @contextlib.contextmanager
    def scoped_time_shift(self, seconds: float):
        """Returns a context manager that adds `seconds` to the clock.

        After the context manager is exited, the time shift is restored
        to its previous value.
        """
        token = time_shift.set(time_shift.get() + seconds)
        try:
            yield
        finally:
            time_shift.reset(token)
