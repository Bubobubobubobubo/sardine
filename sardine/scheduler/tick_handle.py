import asyncio
import functools

@functools.total_ordering
class TickHandle:
    """A handle that allows waiting for a specific tick to pass in the clock."""
    __slots__ = ("when", "fut")

    def __init__(self, tick: int):
        self.when = tick
        self.fut = asyncio.Future()

    def __repr__(self):
        return "<{} {} when={}>".format(
            type(self).__name__,
            "pending"
            if not self.fut.done()
            else "done"
            if not self.fut.cancelled()
            else "cancelled",
            self.when,
        )

    def __eq__(self, other):
        if not isinstance(other, TickHandle):
            return NotImplemented
        return self.when == other.when and self.fut == other.fut

    def __hash__(self):
        return hash((self.when, self.fut))

    def __lt__(self, other):
        if not isinstance(other, TickHandle):
            return NotImplemented
        return self.when < other.when

    def __await__(self):
        return self.fut.__await__()

    def cancel(self):
        return self.fut.cancel()

    def cancelled(self):
        return self.fut.cancelled()
