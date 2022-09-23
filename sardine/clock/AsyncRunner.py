import asyncio
from collections import deque
from dataclasses import dataclass, field
import functools
from rich import print
import inspect
import traceback
from typing import Any, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from . import Clock, TickHandle
    from .Clock import MaybeCoroFunc

__all__ = ("AsyncRunner", "FunctionState")

MAX_FUNCTION_STATES = 3


def _assert_function_signature(sig: inspect.Signature, args, kwargs):
    if args:
        message = "Positional arguments cannot be used in scheduling"
        if missing := _missing_kwargs(sig, args, kwargs):
            message += "; perhaps you meant `{}`?".format(
                ", ".join(f"{k}={v!r}" for k, v in missing.items())
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


def _missing_kwargs(
    sig: inspect.Signature, args: tuple[Any], kwargs: dict[str, Any]
) -> dict[str, Any]:
    required = []
    defaulted = []
    for param in sig.parameters.values():
        if param.kind in (
            param.POSITIONAL_ONLY,
            param.VAR_POSITIONAL,
            param.VAR_KEYWORD,
        ):
            continue
        elif param.name in kwargs:
            continue
        elif param.default is param.empty:
            required.append(param.name)
        else:
            defaulted.append(param.name)

    guessed_mapping = dict(zip(required + defaulted, args))
    return guessed_mapping


async def _maybe_coro(func, *args, **kwargs):
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


@dataclass
class FunctionState:
    func: "MaybeCoroFunc"
    args: tuple
    kwargs: dict


@dataclass
class AsyncRunner:
    """Handles calling synchronizing and running a function in
    the background, with support for run-time function patching.

    This class should only be used through a Clock instance via
    the `Clock.schedule_func()` method.

    The `deferred` parameter is used to control whether AsyncRunner
    runs with an implicit tick shift when calling its function or not.
    This helps improve sound synchronization by giving the function its
    entire delay period to execute rather than a single tick.
    For example, assuming bpm = 120 and ppqn = 48, `deferred=False`
    would require its function to complete within 10ms (1 tick),
    whereas `deferred=True` would allow a function with `d=1`
    to finish execution within 500ms (1 beat) instead.

    In either case, if the function takes too long to execute, it will miss
    its scheduling deadline and cause an unexpected gap between function calls.
    Functions must complete within the time span to avoid this issue.

    """

    clock: "Clock"
    deferred: bool = field(default=True)
    states: list[FunctionState] = field(
        default_factory=functools.partial(deque, maxlen=MAX_FUNCTION_STATES)
    )

    _swimming: bool = field(default=False, repr=False)
    _stop: bool = field(default=False, repr=False)
    _task: Union[asyncio.Task, None] = field(default=None, repr=False)
    _reload_event: asyncio.Event = field(default_factory=asyncio.Event, repr=False)

    def push(self, func: "MaybeCoroFunc", *args, **kwargs):
        """Pushes a function state to the runner to be called in the next iteration."""
        if not self.states:
            return self.states.append(FunctionState(func, args, kwargs))

        last_state = self.states[-1]

        if func is last_state.func:
            # patch the top-most state
            last_state.args = args
            last_state.kwargs = kwargs
        else:
            # transfer arguments from last state if possible
            # (any excess arguments here should be discarded by `_runner()`)
            args = args + last_state.args[len(args) :]
            kwargs = last_state.kwargs | kwargs
            self.states.append(FunctionState(func, args, kwargs))

    def reload(self):
        """Triggers an immediate state reload.

        This method is useful when changes to the clock occur,
        or when a new function is pushed to the runner.

        """
        self._reload_event.set()

    def start(self):
        """Initializes the background runner task.

        :raises RuntimeError:
            This method was called after the task already started.

        """
        if self._task is not None:
            raise RuntimeError("runner task has already started")

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
        self.reload()

    async def _runner(self):
        self.swim()
        last_state = self.states[-1]
        name = last_state.func.__name__
        print(f"[yellow][Init {name}][/yellow]")

        try:
            while self.states and self._swimming and not self._stop:
                # `state.func` must schedule itself to keep swimming
                self._swimming = False
                self._reload_event.clear()
                state = self.states[-1]
                name = state.func.__name__

                if state is not last_state:
                    pushed = len(self.states) > 1 and self.states[-2] is last_state
                    print(
                        f"[yellow][Reloaded {name}]"
                        if pushed
                        else f"[yellow][Restored {name}]"
                    )
                    last_state = state

                signature = inspect.signature(state.func)

                try:
                    _assert_function_signature(signature, state.args, state.kwargs)

                    # Remove any kwargs not present in the new function
                    # (prevents TypeError when user reduces the signature)
                    args = state.args
                    kwargs = _discard_kwargs(signature, state.kwargs)

                    # Introspect arguments to synchronize
                    delay = kwargs.get("d")
                    if delay is None:
                        param = signature.parameters.get("d")
                        delay = getattr(param, "default", 1)

                    if delay <= 0:
                        raise ValueError(f"Delay must be >0, not {delay}")
                except (TypeError, ValueError) as e:
                    print(f"[red][Bad function definition ({name})]")
                    traceback.print_exception(type(e), e, e.__traceback__)
                    self._revert_state()
                    self.swim()
                    continue

                handle = asyncio.ensure_future(self._wait_beats(delay))
                reload = asyncio.ensure_future(self._reload_event.wait())
                done, pending = await asyncio.wait(
                    (handle, reload), return_when=asyncio.FIRST_COMPLETED
                )

                for fut in pending:
                    fut.cancel()
                if reload in done:
                    self.swim()
                    continue

                try:
                    # Use copied context in function by creating it as a task
                    await asyncio.create_task(
                        self._call_func(delay, state.func, args, kwargs),
                        name=f"asyncrunner-func-{name}",
                    )
                except Exception as e:
                    print(f"[red][Function exception | ({name})]")
                    traceback.print_exception(type(e), e, e.__traceback__)
                    self._revert_state()
                    self.swim()
        finally:
            # Remove from clock if necessary
            print(f"[yellow][Stopped {name}]")
            self.clock.runners.pop(name, None)

    async def _call_func(self, delay, func, args, kwargs):
        """Calls the given function and optionally applies an initial
        tick shift of `delay` beats when the `deferred` attribute is
        set to True.
        """
        if self.deferred:
            with self.clock._scoped_tick_shift(1):
                ticks = self.clock.get_beat_ticks(delay)
            self.clock.tick_shift += ticks

        return await _maybe_coro(func, *args, **kwargs)

    def _wait_beats(self, n_beats: Union[float, int]) -> "TickHandle":
        """Returns a TickHandle waiting until one tick before the
        given number of beats is reached.
        """
        clock = self.clock
        with clock._scoped_tick_shift(1):
            ticks = clock.get_beat_ticks(n_beats)
        return clock.wait_after(n_ticks=ticks)

    def _revert_state(self):
        failed = self.states.pop()

        if self.states:
            # patch the global scope so recursive functions don't
            # invoke the failed function
            reverted = self.states[-1]
            failed.func.__globals__[failed.func.__name__] = reverted.func
