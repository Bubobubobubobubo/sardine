import asyncio
from typing import Union

from ...base import BaseHandler
from .time_handle import *

__all__ = ("SleepHandler", "TimeHandle")


class SleepHandler(BaseHandler):
    """The primary interface for other components to sleep."""
    def __init__(self):
        super().__init__()
        self._interrupt_event = asyncio.Event()
        self._wake_event = asyncio.Event()
        self._time_handles: list[TimeHandle] = []

    # Public methods

    async def sleep(self, duration: Union[float, int]):
        # TODO sleep docstring
        clock = self.env.clock
        deadline = clock.time + duration
        func = clock.sleep if clock.can_sleep() else self._sleep

        while True:
            await self._check_termination()
            await self._wake_event.wait()

            duration = deadline - clock.time
            sleep_task = asyncio.create_task(func(duration))
            intrp_task = asyncio.create_task(self._interrupt_event.wait())
            tasks = (sleep_task, intrp_task)

            try:
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            finally:
                for t in tasks:
                    t.cancel()

            if sleep_task in done:
                return

    # Internal methods

    async def _check_termination(self):
        """Cancels the current task if the fish bowl is stopped."""
        # This might be called after teardown, in which case `env` is None
        if self.env is None or not self.env.is_running():
            asyncio.current_task().cancel()

    async def _sleep(self, duration: Union[float, int]):
        clock = self.env.clock
        deadline = clock.time + duration
        # TODO _sleep

    # Handler hooks

    def setup(self):
        for event in ("pause", "resume", "stop"):
            self.register(event)

    def teardown(self):
        self._interrupt_event.set()

    def hook(self, event: str, *args):
        if event == "pause":
            self._interrupt_event.set()
            self._wake_event.clear()
        elif event == "resume":
            self._wake_event.set()
            self._interrupt_event.clear()
        elif event == "stop":
            self._interrupt_event.set()
            self._wake_event.set()  # just in case
