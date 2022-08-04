import asyncio
from collections import deque
from dataclasses import dataclass, field
import functools
from rich import print
import inspect
import traceback
from typing import Any, Callable, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .Clock import Clock

MAX_FUNCTION_STATES = 3


def _assert_function_signature(sig: inspect.Signature, args, kwargs):
    if args:
        message = 'Positional arguments cannot be used in scheduling'
        if missing := _missing_kwargs(sig, args, kwargs):
            message += '; perhaps you meant `{}`?'.format(
                ', '.join(f'{k}={v!r}' for k, v in missing.items())
            )
        raise TypeError(message)


def _discard_kwargs(sig: inspect.Signature, kwargs: dict[str, Any]) -> dict[str, Any]:
    """Discards any kwargs not present in the given signature."""
    MISSING = object()
    pass_through = kwargs.copy()

    for param in sig.parameters.values():
        value = kwargs.get(param.name, MISSING)
        if value is not MISSING:
            pass_through[param.name] = value

    return pass_through


def _missing_kwargs(sig: inspect.Signature, args: tuple[Any], kwargs: dict[str, Any]) -> dict[str, Any]:
    required = []
    defaulted = []
    for param in sig.parameters.values():
        if param.kind in (param.POSITIONAL_ONLY, param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        elif param.name in kwargs:
            continue
        elif param.default is param.empty:
            required.append(param.name)
        else:
            defaulted.append(param.name)

    guessed_mapping = dict(zip(required + defaulted, args))
    return guessed_mapping


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
    states: list[FunctionState] = field(
        default_factory=functools.partial(deque, (), MAX_FUNCTION_STATES)
    )

    _swimming: bool = field(default=False, repr=False)
    _stop: bool = field(default=False, repr=False)
    _task: Union[asyncio.Task, None] = field(default=None, repr=False)

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
        self.swim()
        last_state = self.states[-1]
        name = last_state.func.__name__
        print(f'[yellow][Init {name}][/yellow]')

        try:
            while self.states and self._swimming and not self._stop:
                # `state.func` must schedule itself to keep swimming
                self._swimming = False
                state = self.states[-1]
                name = state.func.__name__

                if state is not last_state:
                    pushed = len(self.states) > 1 and self.states[-2] is last_state
                    print(f'[yellow][Reloaded {name}]' if pushed else f'[yellow][Restored {name}]')
                    last_state = state

                signature = inspect.signature(state.func)

                try:
                    _assert_function_signature(signature, state.args, state.kwargs)

                    # Remove any kwargs not present in the new function
                    # (prevents TypeError when user reduces the signature)
                    args = state.args
                    kwargs = _discard_kwargs(signature, state.kwargs)

                    # Introspect arguments to synchronize
                    delay = kwargs.get('delay')
                    if delay is None:
                        param = signature.parameters.get('delay')
                        delay = getattr(param, 'default', 1)

                    if delay <= 0:
                        raise ValueError(f'Delay must be >0, not {delay}')
                except (TypeError, ValueError) as e:
                    print(f'[red][Bad function definition ({name})]')
                    traceback.print_exception(e)
                    self._revert_state()
                    continue

                await self._wait(delay)

                try:
                    state.func(*args, **kwargs)
                except Exception as e:
                    print(f'[red][Function exception | ({name})]')
                    traceback.print_exception(e)
                    self._revert_state()
                finally:
                    # `self._wait()` usually leaves us exactly 1 tick away
                    # from the next interval. If we don't wait, func() will
                    # be called in an infinite synchronous loop.
                    # A single tick ensures func() can only be called once per tick.
                    await self.clock.wait_after(n_ticks=1)
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
            self.swim()
            # patch the global scope so recursive functions don't
            # invoke the failed function
            reverted = self.states[-1]
            failed.func.__globals__[failed.func.__name__] = reverted.func
