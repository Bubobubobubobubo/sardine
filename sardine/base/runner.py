import asyncio
import concurrent.futures
import threading
from abc import ABC, abstractmethod
from typing import Optional

from .handler import BaseHandler

__all__ = ("BaseRunnerMixin", "BaseThreadedLoopMixin", "BaseRunnerHandler")


class BaseRunnerMixin(ABC):
    """Provides methods for running a background asynchronous function."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._run_task: Optional[asyncio.Task] = None

    @abstractmethod
    async def run(self):
        """The method that will be executed in the background.

        This method must be ready to handle an `asyncio.CancelledError`.
        """

    def is_running(self) -> bool:
        """Indicates if an asyncio task is currently executing `run()`."""
        return self._run_task is not None and not self._run_task.done()

    def start(self) -> bool:
        """Starts the `run()` method in the background.

        Returns:
            bool: True if the task was started, False otherwise.
        """
        allowed = not self.is_running()
        if allowed:
            self._run_task = asyncio.create_task(self.run())
        return allowed

    def stop(self) -> bool:
        """Stops the background task by attempting to cancel it.

        As with any asyncio task, the `run()` method can prevent
        cancellation by catching `asyncio.CancelledError`.

        Returns:
            bool: True if the task was cancelled, False otherwise.
        """
        if self.is_running():
            return self._run_task.cancel()
        return False


class BaseThreadedLoopMixin(BaseRunnerMixin, ABC):
    """Provides methods for running a looping function in another thread.

    Args:
        loop_interval (float):
            The amount of time to sleep between each iteration.
    """

    def __init__(self, *args, loop_interval: float, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop_interval = loop_interval
        self._run_thread: Optional[threading.Thread] = None
        self._completed_event: Optional[asyncio.Event] = None

    @abstractmethod
    def loop(self):
        """Called on every iteration of the loop."""

    @abstractmethod
    def before_loop(self):
        """Called before the loop is about to start."""

    @abstractmethod
    def after_loop(self):
        """Called after the loop has stopped."""

    def _run(self):
        try:
            self.before_loop()

            fut = asyncio.run_coroutine_threadsafe(
                self._completed_event.wait(),
                self._loop
            )

            try:
                while not self._completed_event.is_set():
                    self.loop()

                    try:
                        fut.result(timeout=self.loop_interval)
                    except asyncio.CancelledError:
                        break
                    except concurrent.futures.TimeoutError:
                        pass
            finally:
                self.after_loop()
        finally:
            self._completed_event.set()

    async def run(self):
        self._completed_event = asyncio.Event()
        self._loop = asyncio.get_running_loop()
        self._run_thread = threading.Thread(target=self._run)
        self._run_thread.start()

        try:
            await self._completed_event.wait()
        finally:
            self._completed_event.set()


class BaseRunnerHandler(BaseRunnerMixin, BaseHandler, ABC):
    """Adds automatic starting and stopping to a runner using the handler system.

    Subclasses that override `setup()`, `teardown()`, or `hook()`, must call
    the corresponding super method.
    """
    TRANSPORT_EVENTS = ("start", "stop", "pause", "resume")

    def setup(self):
        for event in self.TRANSPORT_EVENTS:
            self.register(event)

        if self.env.is_running():
            self.start()

    def teardown(self):
        self.stop()

    def hook(self, event: str, *args):
        if event in ("start", "resume"):
            self.start()
        elif event == "stop":
            self.stop()
