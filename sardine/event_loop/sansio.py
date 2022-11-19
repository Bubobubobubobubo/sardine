import asyncio
import threading
from typing import Optional

__all__ = ("SansIOEventLoop", "SansSelector")


class SansSelector:

    _event_list = []

    def __init__(self, wake_cond: threading.Condition):
        self._wake_cond = wake_cond

    def select(self, timeout: Optional[int]):
        timeout = timeout or 0.0
        with self._wake_cond:
            self._wake_cond.wait(timeout)
        return self._event_list


class SansIOEventLoop(asyncio.BaseEventLoop):
    """An event loop implementation with zero I/O support.

    This removes the potential overhead of waiting on I/O from selectors,
    replacing it with `time.sleep()`. Any native I/O APIs will **not** work
    when using this implementation.
    """
    def __init__(self) -> None:
        super().__init__()
        self._wake_cond = wake_cond = threading.Condition()
        self._selector = SansSelector(wake_cond)

    def _process_events(self, event_list):
        pass

    def _write_to_self(self):
        with self._wake_cond:
            self._wake_cond.notify_all()
