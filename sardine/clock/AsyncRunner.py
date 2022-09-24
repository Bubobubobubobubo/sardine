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


def _extract_new_delay(
    sig: inspect.Signature, kwargs: dict[str, Any]
) -> Union[float, int]:
    delay = kwargs.get("d")
    if delay is None:
        param = sig.parameters.get("d")
        delay = getattr(param, "default", 1)

    if not isinstance(delay, (float, int)):
        raise TypeError(f"Delay must be a float or integer, not {delay!r}")
    elif delay <= 0:
        raise ValueError(f"Delay must be >0, not {delay}")

    return delay


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

    interval_shift: int = field(default=0, repr=False)
    """
    The number of ticks to offset the runner's interval.

    An interval defines the number of ticks between each execution
    of the current function. For example, a clock with a ppqn of 24
    and a delay of 2 beats means each interval is 48 ticks.

    Through interval shifting, a function can switch between different
    delays and then compensate for the clock's current tick to avoid
    the next immediate beat being shorter than the expected interval.

    Initially, functions have an interval shift of 0. The runner
    will automatically change its interval shift when the function
    schedules itself with a new delay. This can lead to functions
    with the same delay running at different ticks. To synchronize
    these functions together, their interval shifts should be set
    back to 0 or at least the same value.
    """

    _swimming: bool = field(default=False, repr=False)
    _stop: bool = field(default=False, repr=False)
    _task: Union[asyncio.Task, None] = field(default=None, repr=False)
    _reload_event: asyncio.Event = field(default_factory=asyncio.Event, repr=False)

    _can_correct_delay: bool = field(default=False, repr=False)
    _last_delay: Union[float, int] = field(default=0.0, repr=False)
    # _last_ppqn: int = field(default=0, repr=False)  # TODO ppqn
    _expected_interval: int = field(default=0, repr=False)

    # State management

    def push(self, func: "MaybeCoroFunc", *args, **kwargs):
        """Pushes a function state to the runner to be called in the next iteration."""
        if not self.states:
            state = FunctionState(func, args, kwargs)

            # Once the runner starts it needs the `_last_delay` for interval correction,
            # and since we are in a convenient spot we will populate it here
            signature = inspect.signature(func)
            self._last_delay = _extract_new_delay(signature, kwargs)

            return self.states.append(state)

        last_state = self.states[-1]

        if func is last_state.func:
            # Function reschedule, patch the top-most state
            last_state.args = args
            last_state.kwargs = kwargs
            self._allow_delay_correction()
        else:
            # New function, transfer arguments from last state if possible
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

    # Lifecycle control

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

    # Interval shifting

    def _allow_delay_correction(self):
        """Allows the interval to be corrected in the next iteration."""
        self._can_correct_delay = True

    def _correct_interval(self, delay: Union[float, int]):
        if self._can_correct_delay and delay != self._last_delay:
            # One-off request to update the interval shift
            # so the runner can synchronize to the new interval
            #
            # Similar to what the clock does, we also need to compensate
            # for drift here in case the runner's iteration was too slow
            # or even sub-tick fast
            delta = self.clock.tick - self._expected_interval
            with self.clock._scoped_tick_shift(-delta):
                self.interval_shift = self.clock.get_beat_ticks(delay)

            self._last_delay = delay
            # self._last_delay, self._last_ppqn = delay, self.clock.ppqn

        # TODO handle PPQN changes (or maybe don't?)
        # elif self.clock.ppqn != self._last_ppqn:
        #     # Scale our tick shift to accommodate the increase/decrease
        #     # in number of ticks per interval
        #     n_beats = self.interval_shift / self._last_ppqn
        #     self.interval_shift = n_beats * self.clock.ppqn

        #     self._last_ppqn = self.clock.ppqn

        self._can_correct_delay = False

    async def _runner(self):
        self.swim()
        # self._last_ppqn = self.clock.ppqn  # TODO ppqn
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
                    if pushed:
                        print(f"[yellow][Reloaded {name}]")
                    else:
                        print(f"[yellow][Restored {name}]")
                    last_state = state

                signature = inspect.signature(state.func)

                try:
                    _assert_function_signature(signature, state.args, state.kwargs)

                    # Remove any kwargs not present in the new function
                    # (prevents TypeError when user reduces the signature)
                    args = state.args
                    kwargs = _discard_kwargs(signature, state.kwargs)

                    delay = _extract_new_delay(signature, state.kwargs)
                except (TypeError, ValueError) as e:
                    print(f"[red][Bad function definition ({name})]")
                    traceback.print_exception(type(e), e, e.__traceback__)
                    self._revert_state()
                    self.swim()
                    continue

                self._correct_interval(delay)
                self._expected_interval = self.clock.tick + self._get_corrected_interval(delay)
                # start = self.clock.tick

                handle = asyncio.ensure_future(self._wait_beats(delay))
                reload = asyncio.ensure_future(self._reload_event.wait())
                done, pending = await asyncio.wait(
                    (handle, reload), return_when=asyncio.FIRST_COMPLETED
                )

                # print(
                #     f'{self.clock} AR [green]passed: {self.clock.tick-start}, '
                #     f'started: {start}, shift: {self.interval_shift}, '
                #     f'next: {self._expected_interval}'
                # )

                for fut in pending:
                    fut.cancel()
                if reload in done:
                    self.swim()
                    continue

                try:
                    # Use copied context in function by creating it as a task
                    await asyncio.create_task(
                        self._call_func(state.func, args, kwargs),
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

    def _get_corrected_interval(self, delay: Union[float, int], *, offset: int = 0):
        """Returns the number of ticks until the next `delay` interval,
        offsetted by the `offset` argument.

        This method also adjusts the interval according to the
        `interval_shift` attribute.

        :param delay: The number of beats within each interval.
        :param offset: The number of ticks to offset from the interval.
            A positive offset means the result will be later than
            the actual interval, while a negative offset will be sooner.
        :returns: The number of ticks until the next interval is reached.

        """
        with self.clock._scoped_tick_shift(self.interval_shift - offset):
            return self.clock.get_beat_ticks(delay)

    async def _call_func(self, func, args, kwargs):
        """Calls the given function and optionally applies an initial
        tick shift of 1 beat when the `deferred` attribute is
        set to True.
        """
        if self.deferred:
            ticks = self._get_corrected_interval(1, offset=-1)
            self.clock.tick_shift += ticks

        return await _maybe_coro(func, *args, **kwargs)

    def _wait_beats(self, n_beats: Union[float, int]) -> "TickHandle":
        """Returns a TickHandle waiting until one tick before the
        given number of beats is reached.
        """
        clock = self.clock
        ticks = self._get_corrected_interval(n_beats, offset=-1)
        return clock.wait_after(n_ticks=ticks)

    def _revert_state(self):
        failed = self.states.pop()

        if self.states:
            # patch the global scope so recursive functions don't
            # invoke the failed function
            reverted = self.states[-1]
            failed.func.__globals__[failed.func.__name__] = reverted.func
