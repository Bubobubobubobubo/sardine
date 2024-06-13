import asyncio
import functools

__all__ = ("TimeHandle",)


@functools.total_ordering
class TimeHandle:
    """A handle that can wait for a specified time on the fish bowl's clock."""

    __slots__ = ("when", "fut")

    def __init__(self, deadline: int):
        self.when = deadline
        self.fut = asyncio.get_running_loop().create_future()

    def __repr__(self):
        status = (
            "pending"
            if not self.fut.done()
            else "done" if not self.fut.cancelled() else "cancelled"
        )

        return "<{} {} when={}>".format(
            type(self).__name__,
            status,
            self.when,
        )

    def __eq__(self, other):
        if not isinstance(other, TimeHandle):
            return NotImplemented
        return self.when == other.when and self.fut == other.fut

    def __hash__(self):
        return hash((self.when, self.fut))

    def __lt__(self, other):
        if not isinstance(other, TimeHandle):
            return NotImplemented
        return self.when < other.when

    def __await__(self):
        return self.fut.__await__()

    def cancel(self) -> bool:
        return self.fut.cancel()

    def cancelled(self) -> bool:
        return self.fut.cancelled()

    def done(self) -> bool:
        return self.fut.done()
