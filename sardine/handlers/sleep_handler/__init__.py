import asyncio
import heapq
from typing import Optional, Union

from ...base import BaseHandler
from .time_handle import *

__all__ = ("SleepHandler", "TimeHandle")

NUMBER = Union[float, int]


class SleepHandler(BaseHandler):
    """The primary interface for other components to sleep.

    Args:
        poll_interval (float):
            The polling interval to use when the current clock does not
            support its own method of sleep.
    """

    def __init__(self, poll_interval: float = 0.001):
        super().__init__()

        self.poll_interval = poll_interval

        self._poll_task: Optional[asyncio.Event] = None
        self._interrupt_event = asyncio.Event()
        self._wake_event = asyncio.Event()
        self._time_handles: list[TimeHandle] = []

    # Public methods

    async def sleep(self, duration: NUMBER):
        """Sleeps for the specified duration."""
        deadline = self.env.clock.time + duration
        return await self.sleep_until(deadline)

    async def sleep_until(self, deadline: NUMBER):
        """Sleeps until the given time has been reached.

        The deadline is based on the fish bowl clock's time.
        """
        if self.env is None:
            raise ValueError("SleepHandler must be added to a fish bowl")
        elif not self.env.is_running():
            raise RuntimeError("cannot use sleep until fish bowl has started")

        while True:
            # Handle stop/pauses before proceeding
            if self._is_terminated():
                asyncio.current_task().cancel()
            await self._wake_event.wait()

            clock = self.env.clock

            # Use clock sleep if available, else polling implementation
            if clock.can_sleep():
                sleep_task = asyncio.create_task(
                    clock.sleep(deadline - clock.time)
                )
            else:
                sleep_task = asyncio.create_task(self._sleep_until(deadline))

            # Wait until sleep completes or interruption
            intrp_task = asyncio.create_task(self._interrupt_event.wait())
            tasks = (sleep_task, intrp_task)

            try:
                done, pending = await asyncio.wait(
                    tasks, return_when=asyncio.FIRST_COMPLETED
                )
            finally:
                for t in tasks:
                    t.cancel()

            if sleep_task in done:
                return

    # Internal methods

    def _check_running(self):
        if self._time_handles and not self._is_polling():
            self._poll_task = asyncio.create_task(self._run_poll())
        elif not self._time_handles and self._is_polling():
            self._poll_task.cancel()

    def _create_handle(self, deadline: NUMBER) -> TimeHandle:
        handle = TimeHandle(deadline)

        # `true_time` is used here with the presumption that the deadline
        # already has been time shifted
        if self.env.clock.true_time >= deadline:
            handle.fut.set_result(None)
        else:
            heapq.heappush(self._time_handles, handle)
            self._check_running()

        return handle

    def _is_terminated(self) -> bool:
        # This might be called after teardown, in which case `env` is None
        return self.env is None or not self.env.is_running()

    def _is_polling(self) -> bool:
        return self._poll_task is not None and not self._poll_task.done()

    async def _run_poll(self):
        """Continuously polls the clock's time until all TimeHandles resolve.

        TimeHandles will resolve when their deadline is reached,
        or they are cancelled.

        Note that when a pause/stop occurs, all `sleep_until()` calls
        cancel the `_sleep_until()` task, which should indirectly
        cancel the handle being awaited on.
        """
        # this is implemented very similarly to asyncio.BaseEventLoop
        while self._time_handles:
            while self._time_handles:
                handle = self._time_handles[0]
                if handle.cancelled():
                    heapq.heappop(self._time_handles)
                elif self.env.clock.true_time >= handle.when:
                    handle.fut.set_result(None)
                    heapq.heappop(self._time_handles)
                else:
                    # all handles afterwards are either still waiting or cancelled
                    break
            await asyncio.sleep(self.poll_interval)

    async def _sleep_until(self, deadline: NUMBER):
        await self._create_handle(deadline)

    # Handler hooks

    def setup(self):
        for event in ("pause", "resume", "stop"):
            self.register(event)

    def teardown(self):
        self._interrupt_event.set()
        self._wake_event.set()  # just in case

    def hook(self, event: str, *args):
        if event == "pause":
            self._interrupt_event.set()
            self._wake_event.clear()
        elif event == "resume":
            self._wake_event.set()
            self._interrupt_event.clear()
        elif event == "stop":
            self.teardown()
