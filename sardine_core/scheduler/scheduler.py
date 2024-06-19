from typing import Optional

from sardine_core.base import BaseHandler
from sardine_core.utils import plural

from .async_runner import AsyncRunner

__all__ = ("Scheduler",)


class Scheduler(BaseHandler):
    def __init__(
        self,
        deferred_scheduling: bool = True,
    ):
        super().__init__()
        self._runners: dict[str, AsyncRunner] = {}
        self.deferred = deferred_scheduling

    def _react_to_tempo_change(self, old_tempo: int | float, new_tempo: int | float):
        """
        In reaction to a tempo change, the scheduler should
        trigger an event for each runner prompting to update
        their current interval_shift. This prevents runners
        from desynchronization everytime tempo change happens.
        """
        scale = old_tempo / new_tempo
        for runner in self._runners.values():
            runner.interval_shift *= scale

    def __repr__(self) -> str:
        n_runners = len(self._runners)
        return "<{} ({} {}) deferred={}>".format(
            type(self).__name__,
            n_runners,
            plural(n_runners, "runner"),
            self.deferred,
        )

    @property
    def runners(self) -> list[AsyncRunner]:
        """A list of the current runners stored in the scheduler."""
        return list(self._runners.values())

    # Public methods

    def get_runner(self, name: str) -> Optional[AsyncRunner]:
        """Retrieves the runner with the given name from the scheduler."""
        return self._runners.get(name)

    def start_runner(self, runner: AsyncRunner):
        """Adds the runner to the scheduler and starts it.

        If the runner is already running on the same scheduler,
        this will only update the scheduler's internal reference.

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
                f"A different runner already exists with the name {runner.name!r}"
            )

        self._runners[runner.name] = runner
        runner.scheduler = self
        runner.start()

    def stop_runner(self, runner: AsyncRunner, *, reset_states: bool = True):
        """Removes the runner from the scheduler and stops it.

        Args:
            runner (AsyncRunner): The runner to remove.
            reset_states (bool):
                If True, `AsyncRunner.reset_states()` will be called.

        Raises:
            ValueError: The runner is running on another scheduler.
        """
        if (
            runner.is_running()
            and runner.scheduler is not None
            and runner.scheduler is not self
        ):
            raise ValueError(f"Runner {runner.name!r} is running on another scheduler")

        # We don't set `runner.scheduler = None` because it might
        # break the background task in the process
        runner.stop()
        runner.reload()

        if reset_states:
            runner.reset_states()

        if self._runners.get(runner.name) is runner:
            del self._runners[runner.name]

    def reset(self, *args, **kwargs):
        """Stops and removes all runners from the scheduler.

        Args:
            *args: Positional arguments to be passed to `stop_runner()`.
            **kwargs: Keyword arguments to be passed to `stop_runner()`.
        """
        for runner in self.runners:
            if not runner.background_job:
                self.stop_runner(runner, *args, **kwargs)

    # Internal methods

    def _reload_runners(self, *, interval_correction: bool):
        for runner in self._runners.values():
            runner.reload()

            if interval_correction:
                runner.allow_interval_correction()

    def setup(self):
        self.register("stop")
        self.register("tempo_change")

    def hook(self, event: str, *args):
        if event == "stop":
            self.reset()
        if event == "tempo_change":
            self._react_to_tempo_change(*args)
