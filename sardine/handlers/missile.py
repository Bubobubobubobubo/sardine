import asyncio
from typing import Optional, Union

from ..base import BaseHandler

__all__ = ("MissileMode",)


class MissileMode(BaseHandler):
    """Maximize the current thread's wake time with a CPU-intensive task."""
    def __init__(self, *, burn_rate: Union[float, int] = 1000):
        super().__init__()
        self.burn_interval = 1 / burn_rate
        self._running = False
        self._run_task: Optional[asyncio.Task] = None

    def is_running(self) -> bool:
        return self._run_task is not None and not self._run_task.done()

    async def run(self):
        self._running = True
        while self._running:
            await asyncio.sleep(self.burn_interval)

    # Handler hooks

    def setup(self):
        for event in ("start", "pause", "resume", "stop"):
            self.register(event)

    def teardown(self):
        if self.is_running():
            self._run_task.cancel()

    def hook(self, event: str, *args):
        if event in ("start", "resume") and not self.is_running():
            self._run_task = asyncio.create_task(self.run())
        elif event in ("stop", "pause") and self.is_running():
            self._run_task.cancel()
