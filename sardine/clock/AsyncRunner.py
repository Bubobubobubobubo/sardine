import asyncio
from dataclasses import dataclass, field
from rich import print
import inspect
import traceback
from typing import Any, Callable, TYPE_CHECKING, Union


if TYPE_CHECKING:
    from .Clock import Clock


def _discard_kwargs(sig: inspect.Signature, kwargs: dict[str, Any]) -> dict[str, Any]:
    """Discards any kwargs not present in the given signature."""
    MISSING = object()
    pass_through = kwargs.copy()

    for param in sig.parameters.values():
        value = kwargs.get(param.name, MISSING)
        if value is not MISSING:
            pass_through[param.name] = value

    return pass_through


@dataclass
class FunctionState:
    func: Callable
    args: tuple
    kwargs: dict


@dataclass
class AsyncRunner:
    """Handles calling synchronizing and running a function in
    the background, with support for run-time function patching.

    This class should only be used through a Clock instance via
    the `Clock.schedule()` method.

    """
    clock: "Clock"
    states: list[FunctionState] = field(default_factory=list)

    _swimming: bool = False
    _stop: bool = False
    _task: Union[asyncio.Task, None] = None

    def push(self, func: Callable, *args, **kwargs):
        """Pushes a function state to the runner to be called in
        the next iteration."""
        if not self.states or func is not self.states[-1].func:
            return self.states.append(FunctionState(func, args, kwargs))

        # patch the top-most state
        state = self.states[-1]
        state.args = args
        state.kwargs = kwargs

    def start(self):
        """Initializes the background runner task.

        :raises RuntimeError:
            This method was called after the task already started.

        """
        if self._task is not None:
            raise RuntimeError('runner task has already started')

        self.swim()
        self._task = asyncio.create_task(self._runner())
        self._task.add_done_callback(asyncio.Task.result)

    def started(self) -> bool:
        """Returns True if the runner has been started.

        This method will remain true even if the runner stops afterwards.

        """
        return self._task is not None

    def swim(self):
        """Allows the runner to continue the next iteration.
        This method must be called continuously to keep the runner alive."""
        self._swimming = True

    def stop(self):
        """Stops the runner's execution after the current iteration.

        This method takes precedence when `swim()` is also called.

        """
        self._stop = True

    async def _runner(self):
        last_state = self.states[-1]
        name = last_state.func.__name__
        print(f'[yellow][Init {name}][/yellow]')

        try:
            while self.states and not self._stop:
                # `state.func` must schedule itself to keep swimming
                self._swimming = False
                state = self.states[-1]
                name = state.func.__name__

                if state is not last_state:
                    pushed = len(self.states) > 1 and self.states[-2] is last_state
                    print(f'[yellow][Reloaded {name}]' if pushed else f'[yellow][Restored {name}]')
                    last_state = state

                # Remove any kwargs that aren't present in the new function
                # (prevents TypeError when user reduces the signature)
                signature = inspect.signature(state.func)
                kwargs = _discard_kwargs(signature, kwargs)

                # Introspect arguments to synchronize
                delay = state.kwargs.get('delay')
                if delay is None:
                    param = signature.parameters.get('delay')
                    delay = getattr(param, 'default', 1)

                await self._wait(delay)

                try:
                    state.func(*state.args, **state.kwargs)
                except Exception as e:
                    print(f'Exception encountered in {name}:')
                    traceback.print_exception(e)

                    self._revert_state()
        finally:
            # Remove from clock if necessary
            print(f'[yellow][Stopped {name}]')
            self.clock.runners.pop(name, None)

    async def _wait(self, n_beats: Union[float, int]):
        """Waits until one tick before the given number of beats is reached."""
        clock = self.clock
        ticks = clock.get_beat_ticks(n_beats) - 1
        await clock.wait_after(n_ticks=ticks)

    def _revert_state(self):
        failed = self.states.pop()

        if self.states:
            # patch the global scope so recursive functions don't
            # invoke the failed function
            reverted = self.states[-1]
            failed.func.__globals__[failed.func.__name__] = reverted.func
