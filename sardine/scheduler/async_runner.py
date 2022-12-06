import asyncio
import heapq
import inspect
import traceback
from collections import deque
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, MutableSequence, NamedTuple, Optional, Union

from rich import print
from rich.panel import Panel

from ..base import BaseClock
from ..clock import Time
from ..utils import MISSING
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
    pass_through = kwargs.copy()

    for param in sig.parameters.values():
        value = kwargs.get(param.name, MISSING)
        if value is not MISSING:
            pass_through[param.name] = value

    return pass_through


def _extract_new_period(
    sig: inspect.Signature, kwargs: dict[str, Any]
) -> Union[float, int]:
    period = kwargs.get("p")
    if period is None:
        param = sig.parameters.get("p")
        period = getattr(param, "default", 1)

    if not isinstance(period, (float, int)):
        raise TypeError(f"Period must be a float or integer, not {period!r}")
    elif period <= 0:
        raise ValueError(f"Period must be >0, not {period}")

    return period


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


class DeferredState(NamedTuple):
    deadline: Union[float, int]
    index: int
    state: FunctionState


class AsyncRunner:
    """Handles calling synchronizing and running a function in
    the background, with support for run-time function patching.

    Runners should only be started from the `Scheduler.start_runner()` method.

    The `Scheduler.deferred` attribute is used to control if AsyncRunner
    runs with an implicit time shift when calling its function or not.
    This helps improve sound synchronization by giving the function
    more time to execute. For example, assuming bpm = 120, `deferred=False`
    would expect its function to complete instantaneously,
    whereas `deferred=True` would allow a function with `p=1`
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
    deferred_states: list[DeferredState]
    """
    A heap queue storing (time, index, state) pairs.

    Unlike regular `states`, these states are left in the background until
    their time arrives, at which point they are moved to the `states` sequence
    and will take over the next iteration.
    """
    interval_shift: float
    """
    The amount of time to offset the runner's interval.

    An interval defines the amount of time between each execution
    of the current function. For example, a clock with a beat duration
    of 0.5s and a period of 2 beats means each interval is 1 second.

    Through interval shifting, a function can switch between different
    periods/tempos and then compensate for the clock's current time to
    avoid the next immediate beat being shorter than expected.

    Initially, functions have an interval shift of 0. The runner
    will automatically change its interval shift when the function
    schedules itself with a new period or a change in the clock's beat
    duration occurs. This can lead to functions with the same period
    running at different phases. To synchronize these functions together,
    their interval shifts should be set to the same value (usually 0).
    """
    snap: Optional[Union[float, int]]
    """
    The absolute time that the next interval should start at.

    Setting this attribute will take priority over the regular interval
    on the next iteration and cause the runner to wait until the snap
    deadline has arrived.

    The `delay_interval()` method combines this with interval shifting
    to properly delay a runner and its interval until the given deadline.

    Once this time has been passed and the next iteration was run,
    this attribute will be reset to `None`.

    Note that deferred states will take priority over this, and in fact even
    replace the snap, if one or more of those states specify a deadline earlier
    than the current snap's deadline.
    """

    _swimming: bool
    _stop: bool
    _task: Optional[asyncio.Task]
    _reload_event: asyncio.Event
    _has_reverted: bool

    _deferred_state_index: int

    _can_correct_interval: bool
    _delta: float
    _expected_time: float
    _last_interval: float
    _last_state: Optional[FunctionState]
    _sleep_drift: float

    def __init__(self, name: str):
        self.name = name
        self.scheduler = None
        self.states = deque(maxlen=self.MAX_FUNCTION_STATES)
        self.deferred_states = []
        self.interval_shift = 0.0
        self.snap = None

        self._swimming = False
        self._stop = False
        self._task = None
        self._reload_event = asyncio.Event()
        self._has_reverted = False

        self._deferred_state_index = 0

        self._can_correct_interval = False
        self._delta = 0.0
        self._expected_time = 0.0
        self._last_interval = 0.0
        self._last_state = None
        self._sleep_drift = 0.0

    def __repr__(self):
        cls_name = type(self).__name__
        status = "running" if self.is_running() else "stopped"
        attrs = " ".join(
            f"{attr}={getattr(self, attr)!r}"
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
        """Pushes a function state to the runner to be called in the next iteration.

        It is recommended to reload the runner after this in case the
        current iteration sleeps past the deadline.

        Note that this does not take priority over the `snap` attribute;
        if a snap is specified, the runner will continue to wait for that
        deadline to pass. If running a new function immediately is desired,
        the `snap` should be set to `None` before reloading the runner.

        Args:
            func (MaybeCoroFunc): The function to add.
            *args: The positional arguments being passed to `func`.
            **kwargs: The keyword arguments being passed to `func`.
        """
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

    def push_deferred(
        self, deadline: Union[float, int], func: "MaybeCoroFunc", *args, **kwargs
    ):
        """Adds a function to a queue to eventually be run.

        It is recommended to reload the runner after this in case the
        current iteration sleeps past the deadline.

        If there is an existing `snap` deadline, deferred states will take
        priority and replace the `snap` attribute to ensure they run on time.

        Args:
            time (Union[float, int]):
                The absolute clock time to wait before the function state
                is pushed.
            func (MaybeCoroFunc): The function to add.
            *args: The positional arguments being passed to `func`.
            **kwargs: The keyword arguments being passed to `func`.
        """
        if not callable(func):
            raise TypeError(f"Expected a callable, got {func!r}")

        if not self.deferred_states:
            self._deferred_state_index = 0

        index = self._deferred_state_index
        self._deferred_state_index += 1

        state = FunctionState(func, args, kwargs)
        heapq.heappush(self.deferred_states, DeferredState(deadline, index, state))

    def update_state(self, *args, **kwargs):
        """Updates the top-most function state with new arguments.

        This assumes that the function is rescheduling itself, and
        will therefore allow interval correction to occur in case
        the period or tempo has changed.
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

    def reset_states(self):
        """Clears all function states from the runner.

        This method can safely be called while the runner is running.
        In such case, the runner will stop by itself on the next
        iteration unless a new state is pushed after this method.
        """
        self.states.clear()
        self.deferred_states.clear()

    # Interval shifting

    def allow_interval_correction(self):
        """Allows the interval to be corrected in the next iteration."""
        self._can_correct_interval = True

    def delay_interval(self, deadline: Union[float, int], period: Union[float, int]):
        """Delays the next iteration until the given deadline has passed.

        This is equivalent to setting the runner's `snap` attribute
        to the deadline and also applying an appropriate interval
        shift to synchronize the period.

        The runner must be started from a scheduler before this method can
        be used. In addition, at least one function state must be pushed to
        the runner (deferred or not) in order to calculate the interval shift.

        To take effect immediately, the runner should be reloaded
        to skip the current iteration.

        Args:
            time (Union[float, int]): The absolute time to wait.
            period (Union[float, int]): The period to synchronize to.

        Raises:
            RuntimeError: A function must be pushed before this can be used.
        """
        self.snap = deadline
        # Unlike _correct_interval(), we don't need to worry about delta
        # here. _get_corrected_interval() ignores the interval until the
        # snap time has passed, at which point any sleep drift will be
        # accounted by `get_beat_time()` as per normal operation.
        with self.time.scoped_shift(deadline - self.clock.time):
            self.interval_shift = self.clock.get_beat_time(period)

    def _correct_interval(self, period: Union[float, int]):
        """Checks if the interval should be corrected.

        Interval correction occurs when `allow_interval_correction()`
        is called, and the given interval is different from the last
        interval *only* for the current iteration. If the interval
        did not change, interval correction must be requested again.

        Args:
            period (Union[float, int]):
                The period being used in the current iteration.
        """
        interval = period * self.clock.beat_duration
        if self._can_correct_interval and interval != self._last_interval:
            with self.time.scoped_shift(-self._delta):
                self.interval_shift = self.clock.get_beat_time(period)

        self._last_interval = interval
        self._can_correct_interval = False

    def _get_corrected_interval(self, period: Union[float, int]) -> float:
        """Returns the amount of time until the next interval.

        The base interval is determined by the `period` argument,
        and then offsetted by the `interval_shift` attribute.

        If the `snap` attribute is set to an absolute time
        and the current clock time has not passed the snap,
        it will take priority over whatever period was passed.

        Args:
            period (Union[float, int]):
                The number of beats in the interval.

        Returns:
            float: The amount of time until the next interval is reached.
        """
        snap_duration = self._get_snap_duration()
        if snap_duration is not None:
            return snap_duration

        with self.time.scoped_shift(self.interval_shift - self._delta):
            # If the interval was corrected, this should equal to:
            #    `period * beat_duration`
            expected_duration = self.clock.get_beat_time(period)
            self._expected_time = self.clock.shifted_time + expected_duration
        return expected_duration - self._delta

    def _get_snap_duration(self) -> Optional[float]:
        """Returns the amount of time to wait for the snap, if any.

        If the `snap` attribute is None, this returns None.
        """
        if self.snap is None:
            return None
        return max(0.0, self.snap - self.clock.time)

    # Runner loop

    async def _runner(self):
        # Prepare to swim
        self._last_state = self._get_state()
        self._swimming = True
        self._stop = False
        self._delta = 0.0

        period = self._get_period(self._last_state)
        self._get_corrected_interval(period)  # sets `_expected_time`
        self._last_interval = period * self.clock.beat_duration

        print_panel(f"[yellow][[red]{self.name}[/red] is swimming][/yellow]")

        try:
            while self._is_ready_for_iteration():
                await self._run_once()
        finally:
            print_panel(f"[yellow][Stopped [red]{self.name}[/red]][/yellow]")

    async def _run_once(self):
        self._swimming = False
        self._reload_event.clear()

        state = self._get_state()

        if state is not None:
            self._maybe_print_new_state(state)
            self._last_state = state
            signature = inspect.signature(state.func)

            try:
                _assert_function_signature(signature, state.args, state.kwargs)
                args = state.args
                # Prevent any TypeErrors when the user reduces the signature
                kwargs = _discard_kwargs(signature, state.kwargs)
                period = _extract_new_period(signature, state.kwargs)
            except (TypeError, ValueError) as exc:
                print(f"[red][Bad function definition ({self.name})]")
                traceback.print_exception(type(exc), exc, exc.__traceback__)

                self._revert_state()
                self.swim()
                return

            self._correct_interval(period)
            duration = self._get_corrected_interval(period)
            self._expected_time = self.clock.time + duration

        # Push any deferred states that have or will arrive onto the stack
        arriving_states: list[DeferredState] = []
        while self.deferred_states:
            entry = self.deferred_states[0]
            if (
                self.clock.time >= entry.deadline
                or state is not None
                and self._expected_time >= entry.deadline
            ):
                heapq.heappop(self.deferred_states)
                arriving_states.append(entry)
            else:
                break

        if arriving_states:
            latest_entry = arriving_states[-1]
            self.states.extend(e.state for e in arriving_states)
            # In case the new state has a faster interval than before,
            # delay it so it doesn't run too early
            self.delay_interval(
                latest_entry.deadline,
                self._get_period(latest_entry.state),
            )
            self.swim()
            return
        elif state is None:
            # Nothing to do until the next deferred state arrives
            deadline = self.deferred_states[0].deadline
            duration = self.clock.time - deadline
            interrupted = await self._sleep(duration)
            self.swim()
            return

        # NOTE: duration will always be defined at this point
        interrupted = await self._sleep(duration)
        if interrupted:
            self.swim()
            return

        try:
            # Use copied context in function by creating it as a task
            await asyncio.create_task(
                self._call_func(state.func, args, kwargs),
                name=f"asyncrunner-func-{self.name}",
            )
        except Exception as exc:
            print(f"[red][Function exception | ({self.name})]")
            traceback.print_exception(type(exc), exc, exc.__traceback__)

            self._revert_state()
            self.swim()

        self._delta = self.clock.time - self._expected_time
        self._check_snap()

    async def _call_func(self, func, args, kwargs):
        """Calls the given function and optionally applies time shift
        according to the `defer_beats` attribute.
        """
        shift = self.defer_beats * self.clock.beat_duration - self._sleep_drift
        self.time.shift += shift

        return await _maybe_coro(func, *args, **kwargs)

    def _check_snap(self) -> None:
        if self.snap is not None and self.clock.time > self.snap:
            self.snap = None

    @staticmethod
    def _get_period(state: Optional[FunctionState]) -> Union[float, int]:
        if state is None:
            return 0.0

        return _extract_new_period(inspect.signature(state.func), state.kwargs)

    def _get_state(self) -> Optional[FunctionState]:
        return self.states[-1] if self.states else None

    def _is_ready_for_iteration(self) -> bool:
        return (
            (self.states or self.deferred_states)
            and self._swimming  # self.swim()
            and not self._stop  # self.stop()
        )

    def _maybe_print_new_state(self, state: FunctionState):
        if self._last_state is not None and state is not self._last_state:
            if not self._has_reverted:
                print_panel(f"[yellow][Updating [red]{self.name}[/red]]")
            else:
                print_panel(f"[yellow][Saving [red]{self.name}[/red] from crash]")
                self._has_reverted = False

    async def _sleep(self, duration: Union[float, int]) -> bool:
        """Sleeps for the given duration or until the runner is reloaded.

        Args:
            duration (Union[float, int]): The amount of time to sleep.

        Returns:
            bool: True if the runner was reloaded, False otherwise.
        """
        if duration <= 0:
            return self._reload_event.is_set()

        wait_task = asyncio.create_task(self.env.sleep(duration))
        reload_task = asyncio.create_task(self._reload_event.wait())
        done, pending = await asyncio.wait(
            (wait_task, reload_task),
            return_when=asyncio.FIRST_COMPLETED,
        )

        self._sleep_drift = self.clock.time - self._expected_time

        for task in pending:
            task.cancel()
        for task in done:
            task.result()

        return reload_task in done

    def _revert_state(self):
        self.states.pop()
        self._has_reverted = True
