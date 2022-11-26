import inspect

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
        self.runners: dict[str, AsyncRunner] = {}
        self.deferred = deferred_scheduling
        self._events = {
            "tempo_update": self.on_tempo_update,
        }

    def __repr__(self) -> str:
        n_runners = len(self.runners)
        return "<{} ({} {}) deferred={}>".format(
            type(self).__name__,
            n_runners,
            plural(n_runners, "runner"),
            self.deferred,
        )

    # Public methods

    def schedule_func(self, func: MaybeCoroFunc, /, *args, **kwargs):
        """Schedules the given function to be executed."""
        if not (inspect.isfunction(func) or inspect.ismethod(func)):
            raise TypeError(f"func must be a function, not {type(func).__name__}")

        name = func.__name__
        runner = self.runners.get(name)
        if runner is None:
            runner = self.runners[name] = AsyncRunner(scheduler=self)

        runner.push(func, *args, **kwargs)
        if runner.started():
            runner.reload()
            runner.swim()
        else:
            runner.start()

    def remove(self, func: MaybeCoroFunc, /):
        """Schedules the given function to stop execution."""
        runner = self.runners.get(func.__name__)
        if runner is not None:
            runner.stop()

    def print_children(self):
        """Print all children on clock"""
        [print(child) for child in self.runners]

    def reset(self):
        for runner in self.runners.values():
            runner.stop()
        self.runners.clear()

    # Internal methods

    def _reload_runners(self):
        for runner in self.runners.values():
            runner.reload()

    # Handler hooks

    def setup(self):
        for event in self._events:
            self.register(event)

    def hook(self, event: str, *args):
        func = self._events[event]
        func(*args)

    def on_tempo_update(self, old: float, new: float):
        # Let runners re-calculate their next interval sooner
        self._reload_runners()
