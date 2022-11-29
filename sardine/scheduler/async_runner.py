import asyncio
import inspect
import traceback
from collections import deque
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, MutableSequence, Optional, Union

from rich import print
from rich.panel import Panel

from ..base import BaseClock
from ..clock import Time
from .constants import MaybeCoroFunc

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl
    from .scheduler import Scheduler

__all__ = ("AsyncRunner", "FunctionState")


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

    MAX_FUNCTION_STATES = 3

    name: str
    """Uniquely identifies a runner when it is added to a scheduler."""

    scheduler: "Optional[Scheduler]"
    """The scheduler this runner was added to."""
    states: MutableSequence[FunctionState]
    """
    The function stack, used for auto-restoring functions.

    This is implemented with a deque to ensure a limit on how many functions
    are stored in the cache.
    """
    interval_shift: float
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

    _swimming: bool
    _stop: bool
    _task: Optional[asyncio.Task]
    _reload_event: asyncio.Event

    _can_correct_interval: bool
    _delta: float
    _expected_time: float
    _last_interval: float

    def __init__(self, name: str):
        self.name = name
        self.scheduler = None
        self.states = deque(maxlen=self.MAX_FUNCTION_STATES)
        self.interval_shift = 0.0

        self._swimming = False
        self._stop = False
        self._task = None
        self._reload_event = asyncio.Event()

        self._can_correct_interval = False
        self._delta = 0.0
        self._expected_time = 0.0
        self._last_interval = 0.0

    def __repr__(self):
        cls_name = type(self).__name__
        status = ("running" if self.is_running() else "stopped")
        attrs = " ".join(
            f"{attr}={getattr(self, attr)}"
            for attr in (
                "name",
                "scheduler",
            )
        )
        return f"<{cls_name} {status} {attrs}>"

    # Helper properties

    @property
    def clock(self) -> BaseClock:
        """A shorthand for the current clock."""
        return self.scheduler.env.clock

    @property
    def defer_beats(self) -> float:
        """The number of beats to defer function calls."""
        return float(self.scheduler.deferred)

    @property
    def env(self) -> "FishBowl":
        """A shorthand for the scheduler's fish bowl."""
        return self.scheduler.env

    @property
    def time(self) -> Time:
        """The fish bowl's current time."""
        return self.scheduler.env.time

    # State management

    def push(self, func: "MaybeCoroFunc", *args, **kwargs):
        """Pushes a function state to the runner to be called in the next iteration."""
        if not callable(func):
            raise TypeError(f"Expected a callable, got {func!r}")
        elif not self.states:
            state = FunctionState(func, args, kwargs)
            return self.states.append(state)

        last_state = self.states[-1]

        # Transfer arguments from last state if possible
        # (`_runner()` will discard excess arguments later)
        args = args + last_state.args[len(args) :]
        kwargs = last_state.kwargs | kwargs
        self.states.append(FunctionState(func, args, kwargs))

    def update_state(self, *args, **kwargs):
        """Updates the top-most function state with new arguments.

        This assumes that the function is rescheduling itself, and
        will therefore allow interval correction to occur in case
        the delay or tempo has changed.
        """
        last_state = self.states[-1]
        last_state.args = args
        last_state.kwargs = kwargs
        self.allow_interval_correction()

    def reload(self):
        """Triggers an immediate state reload.

        This method is useful when changes to the clock occur,
        or when a new function is pushed to the runner.
        """
        self._reload_event.set()

    # Lifecycle control

    def start(self):
        """Initializes the background runner task.

        If the task has already started, this is a no-op.
        """
        if self.is_running():
            return

        self._task = asyncio.create_task(self._runner())
        self._task.add_done_callback(asyncio.Task.result)

    def is_running(self) -> bool:
        """Returns True if the runner is running."""
        return self._task is not None and not self._task.done()

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
        # Prepare to swim
        last_state = self.states[-1]
        self._swimming = True
        self._stop = False

        # Calculate the initial value for `_last_interval`
        self._last_interval = (
            _extract_new_delay(inspect.signature(last_state.func), last_state.kwargs)
            * self.clock.beat_duration
        )

        print_panel(f"[yellow][[red]{self.name}[/red] is swimming][/yellow]")

        try:
            while self.states and self._swimming and not self._stop:
                self._swimming = False
                self._reload_event.clear()
                state = self.states[-1]

                if state is not last_state:
                    pushed = len(self.states) > 1 and self.states[-2] is last_state
                    if pushed:
                        print_panel(f"[yellow][Updating [red]{self.name}[/red]]")
                    else:
                        print_panel(
                            f"[yellow][Saving [red]{self.name}[/red] from crash]"
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
                    print(f"[red][Bad function definition ({self.name})]")
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
                        name=f"asyncrunner-func-{self.name}",
                    )
                except Exception as e:
                    print(f"[red][Function exception | ({self.name})]")
                    traceback.print_exception(type(e), e, e.__traceback__)
                    self._revert_state()
                    self.swim()

                self._delta = self.clock.time - self._expected_time
        finally:
            print_panel(f"[yellow][Stopped [red]{self.name}[/red]][/yellow]")

    async def _call_func(self, delta: float, func, args, kwargs):
        """Calls the given function and optionally applies time shift
        according to the `defer_beats` attribute.
        """
        shift = self.defer_beats * self.clock.beat_duration - delta
        self.time.shift += shift

        return await _maybe_coro(func, *args, **kwargs)

    def _revert_state(self):
        self.states.pop()
