import asyncio
import functools
import inspect
import traceback
from collections import deque
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Union

from rich import print
from rich.panel import Panel

from ..base import BaseClock
from ..clock import Time
from .constants import MaybeCoroFunc

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl
    from .scheduler import Scheduler

__all__ = ("AsyncRunner", "FunctionState")

MAX_FUNCTION_STATES = 3


def print_panel(text: str) -> None:
    """
    Print swimming function event inside a Rich based Panel.
    The box is automatically resized to fit text length.
    """
    print("\n", Panel.fit(text), end="")


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

    This class should only be used through a BaseClock instance via
    the `BaseClock.schedule_func()` method.

    The `Scheduler.deferred` attribute is used to control if AsyncRunner
    runs with an implicit time shift when calling its function or not.
    This helps improve sound synchronization by giving the function
    more time to execute. For example, assuming bpm = 120, `deferred=False`
    would expect its function to complete instantaneously,
    whereas `deferred=True` would allow a function with `d=1`
    to finish execution within 500ms (1 beat) instead.

    In either case, if the function takes too long to execute, it will miss
    its scheduling deadline and cause an unexpected gap between function calls.
    Functions must complete within the time span to avoid this issue.

    """

    scheduler: "Scheduler"
    states: list[FunctionState] = field(
        default_factory=functools.partial(deque, maxlen=MAX_FUNCTION_STATES)
    )

    interval_shift: float = field(default=0.0, repr=False)
    """
    The amount of time to offset the runner's interval.

    An interval defines the amount of time between each execution
    of the current function. For example, a clock with a beat duration
    of 0.5s and a delay of 2 beats means each interval is 1 second.

    Through interval shifting, a function can switch between different
    delays/tempos and then compensate for the clock's current time to
    avoid the next immediate beat being shorter than expected.

    Initially, functions have an interval shift of 0. The runner
    will automatically change its interval shift when the function
    schedules itself with a new delay or a change in the clock's beat
    duration occurs. This can lead to functions with the same delay
    running at different phases. To synchronize these functions together,
    their interval shifts should be set to the same value (usually 0).
    """

    _swimming: bool = field(default=False, repr=False)
    _stop: bool = field(default=False, repr=False)
    _task: Union[asyncio.Task, None] = field(default=None, repr=False)
    _reload_event: asyncio.Event = field(default_factory=asyncio.Event, repr=False)

    _can_correct_interval: bool = field(default=False, repr=False)
    _delta: float = field(default=0.0, repr=False)
    _expected_time: float = field(default=0.0, repr=False)
    _last_interval: float = field(default=0.0, repr=False)

    # Helper properties

    @property
    def clock(self) -> BaseClock:
        return self.scheduler.env.clock

    @property
    def defer_beats(self) -> float:
        """The number of beats to defer function calls."""
        return float(self.scheduler.deferred)

    @property
    def env(self) -> "FishBowl":
        return self.scheduler.env

    @property
    def time(self) -> Time:
        """The fish bowl's current time."""
        return self.scheduler.env.time

    # State management

    def push(self, func: "MaybeCoroFunc", *args, **kwargs):
        """Pushes a function state to the runner to be called in the next iteration."""
        if not self.states:
            state = FunctionState(func, args, kwargs)

            # Once the runner starts it needs the `_last_delay` for interval correction,
            # and since we are in a convenient spot we will populate it here
            delay = _extract_new_delay(inspect.signature(func), kwargs)
            self._last_interval = delay * self.clock.beat_duration

            return self.states.append(state)

        last_state = self.states[-1]

        if func is last_state.func:
            # Function reschedule, patch the top-most state
            last_state.args = args
            last_state.kwargs = kwargs
            self.allow_interval_correction()
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

        Raises:
            RuntimeError: This method was called after the task already started.
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

        This method must be called continuously to keep the runner alive.
        """
        self._swimming = True

    def stop(self):
        """Stops the runner's execution after the current iteration.

        This method takes precedence when `swim()` is also called.
        """
        self._stop = True
        self.reload()

    # Interval shifting

    def allow_interval_correction(self):
        """Allows the interval to be corrected in the next iteration."""
        self._can_correct_interval = True

    def _correct_interval(self, delay: Union[float, int]):
        """Checks if the interval should be corrected.

        Interval correction occurs when `allow_interval_correction()`
        is called, and the given interval is different from the last
        interval *only* for the current iteration. If the interval
        did not change, interval correction must be requested again.

        Args:
            delay (Union[float, int]):
                The delay being used in the current iteration.
        """
        interval = delay * self.clock.beat_duration
        if self._can_correct_interval and interval != self._last_interval:
            self.interval_shift = self.clock.get_beat_time(delay) + self._delta

            self._last_interval = interval

        self._can_correct_interval = False

    def _get_corrected_interval(self, delay: Union[float, int]) -> float:
        """Returns the amount of time until the next interval.

        The base interval is determined by the `delay` argument,
        and then offsetted by the `interval_shift` attribute.

        Args:
            delay (Union[float, int]):
                The number of beats in the interval.

        Returns:
            float: The amount of time until the next interval is reached.
        """
        with self.time.scoped_shift(self.interval_shift):
            return self.clock.get_beat_time(delay)

    # Runner loop

    async def _runner(self):
        """The entry point for AsyncRunner. This can only be started
        once per AsyncRunner instance through the `start()` method.

        Drift correction
        ----------------
        In this loop, there is a potential for drift to occur anywhere with
        an async/await keyword. The relevant steps here are:

            1. Correct interval
            2. (await) Sleep until interval
            3. (await) Call function
            4. Repeat

        Step 2 tends to add a bit of latency (a result of `asyncio.wait()`).
        When using deferred scheduling, step 3 subtracts that drift to make
        sure sounds are still scheduled for the correct time.

        Step 3 usually adds drift too, and slow functions can further increase
        this drift. However, we don't need to measure the drift here
        because the upcoming call to `BaseClock.get_beat_time()` in step 2
        will synchronize the interval for us.
        """
        self.swim()
        last_state = self.states[-1]
        name = last_state.func.__name__
        if name != "_global_runner":
            print_panel(f"[yellow][[red]{name}[/red] is swimming][/yellow]")

        try:
            while self.states and self._swimming and not self._stop:
                # `state.func` must schedule itself to keep swimming
                self._swimming = False
                self._reload_event.clear()
                state = self.states[-1]
                name = state.func.__name__

                if state is not last_state:
                    pushed = len(self.states) > 1 and self.states[-2] is last_state
                    if name != "_global_runner":
                        if pushed:
                            print_panel(f"[yellow][Updating [red]{name}[/red]]")
                        else:
                            print_panel(
                                f"[yellow][Saving [red]{name}[/red] from crash]"
                            )
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


                # start = self.clock.time

                self._correct_interval(delay)
                duration = self._get_corrected_interval(delay)
                self._expected_time = self.clock.time + duration

                wait_task = asyncio.create_task(self.env.sleep(duration))
                reload_task = asyncio.create_task(self._reload_event.wait())
                done, pending = await asyncio.wait(
                    (wait_task, reload_task),
                    return_when=asyncio.FIRST_COMPLETED,
                )

                sleep_drift = self.clock.time - self._expected_time

                # print(
                #     f"{self.clock} AR [green]"
                #     f"expected: {self._expected_interval}, previous: {start}, "
                #     f"delta: {self._delta}, shift: {self.interval_shift}, "
                #     f"post drift: {sleep_drift}"
                # )

                for fut in pending:
                    fut.cancel()
                if reload_task in done:
                    self.swim()
                    continue

                try:
                    # Use copied context in function by creating it as a task
                    await asyncio.create_task(
                        self._call_func(sleep_drift, state.func, args, kwargs),
                        name=f"asyncrunner-func-{name}",
                    )
                except Exception as e:
                    print(f"[red][Function exception | ({name})]")
                    traceback.print_exception(type(e), e, e.__traceback__)
                    self._revert_state()
                    self.swim()

                self._delta = self.clock.time - self._expected_time
        finally:
            # Remove from clock if necessary
            print_panel(f"[yellow][Stopped [red]{name}[/red]][/yellow]")
            self.scheduler.runners.pop(name, None)

    async def _call_func(self, delta: float, func, args, kwargs):
        """Calls the given function and optionally applies time shift
        according to the `defer_beats` attribute.
        """
        shift = self.defer_beats * self.clock.beat_duration - delta
        self.time.shift += shift

        return await _maybe_coro(func, *args, **kwargs)

    def _revert_state(self):
        failed = self.states.pop()

        if self.states:
            # patch the global scope so recursive functions don't
            # invoke the failed function
            reverted = self.states[-1]
            failed.func.__globals__[failed.func.__name__] = reverted.func
