import inspect
from typing import Optional

from rich import print

from ..base import BaseHandler
from ..utils import plural
from .async_runner import AsyncRunner
from .constants import MaybeCoroFunc

__all__ = ("Scheduler",)


class Scheduler(BaseHandler):
    def __init__(
        self,
        deferred_scheduling: bool = True,
    ):
        super().__init__()
        self._runners: dict[str, AsyncRunner] = {}
        self.deferred = deferred_scheduling

    def __repr__(self) -> str:
        n_runners = len(self._runners)
        return "<{} ({} {}) deferred={}>".format(
            type(self).__name__,
            n_runners,
            plural(n_runners, "runner"),
            self.deferred,
        )

    # Public methods

    def get_runner(self, name: str) -> Optional[AsyncRunner]:
        """Retrieves the runner with the given name from the scheduler."""
        return self._runners.get(name)

    def start_runner(self, runner: AsyncRunner):
        """Adds the runner to the scheduler and starts it.

        If the runner is already running on the same scheduler,
        this will update the scheduler's internal reference
        to the runner, but otherwise do nothing.

        Args:
            runner (AsyncRunner): The runner to schedule and start.

        Raises:
            ValueError:
                The runner is either running on another scheduler or
                has a name conflicting with a different runner instance.
        """
        if (
            runner.is_running()
            and runner.scheduler is not None
            and runner.scheduler is not self
        ):
            raise ValueError(f"Runner {runner.name!r} is running on another scheduler")

        old = self.get_runner(runner.name)
        if old is not None and old is not runner:
            raise ValueError(
                f"Runner {runner.name!r} conflicts with the name "
                "of an existing runner"
            )

        self._runners[runner.name] = runner
        runner.scheduler = self
        runner.start()

    def stop_runner(self, runner: AsyncRunner):
        """Removes the runner from the scheduler and stops it.

        Note that this does not remove the runner's reference to
        the scheduler until it is garbage collected.

        Args:
            runner (AsyncRunner): The runner to remove.

        Raises:
            ValueError: The runner is running on another scheduler.
        """
        if (
            runner.is_running()
            and runner.scheduler is not None
            and runner.scheduler is not self
        ):
            raise ValueError(f"Runner {runner.name!r} is running on another scheduler")

        runner.stop()

        if self._runners.get(runner.name) is runner:
            del self._runners[runner.name]

    def print_children(self):
        """Print all children on clock"""
        [print(child) for child in self._runners]

    def reset(self):
        for runner in tuple(self._runners.values()):
            self.stop_runner(runner)

    # Internal methods

    def _reload_runners(self, *, interval_correction: bool):
        for runner in self._runners.values():
            runner.reload()

            if interval_correction:
                runner.allow_interval_correction()

    # Handler hooks

    def setup(self):
        for event in ("tempo_update",):
            self.register(event)

    def hook(self, event: str, *args):
        if event == "tempo_update":
            self._reload_runners(interval_correction=True)
