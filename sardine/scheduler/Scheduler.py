import contextlib
import heapq
import inspect
from typing import Awaitable, Callable, Optional, TypeVar, Union

from rich import print

from ..base import BaseHandler
from .async_runner import AsyncRunner
from .tick_handle import TickHandle

__all__ = ("Scheduler",)

T = TypeVar("T")
MaybeCoroFunc = Callable[..., Union[T, Awaitable[T]]]


class Scheduler(BaseHandler):
    def __init__(
        self,
        deferred_scheduling: bool = True,
    ):
        self.runners: dict[str, AsyncRunner] = {}
        self.tick_handles: list[TickHandle] = []
        self.deferred = deferred_scheduling

    # TODO: Scheduler.__repr__

    def setup(self):
        self.register('tick')

    def hook(self, event: str, *args):
        if event == 'tick':
            self._update_handles()

    # ---------------------------------------------------------------------- #
    # Clock properties

    # @property
    # def nudge(self) -> int:
    #     return self._nudge

    # @nudge.setter
    # def nudge(self, value: int):
    #     """
    #     Nudge the clock to align on another peer. Very similar to accel
    #     but temporary. Nudge will reset every time the clock loops around.

    #     Args:
    #         value (int): nudge factor
    #     """
    #     self._nudge = value
    #     self._reload_runners()

    @property
    def tick(self) -> int:
        return self._current_tick + self.tick_shift

    @tick.setter
    def tick(self, new_tick: int) -> int:
        """
        Tick is the tiniest grain of time recognized by the Sardine Clock.
        A tick is the time taken by the clock to loop on itself. Ticks are
        used to deduce all other temporal informations: beat, bar, etc...
        They are also sometimes used to compute duration of a given event.

        Args:
            new_tick (int): give a new tick (backwards or forward in time)
        """
        change = new_tick - self._current_tick
        self._current_tick = new_tick
        self._shift_handles(change)
        self._reload_runners()
        self._update_handles()

    # TODO: reload_runners on ppqn change

    def get_beat_ticks(self, n_beats: Union[int, float], *, sync: bool = True) -> int:
        """Determines the number of ticks to wait for N beats to pass.

        :param n_beats: The number of beats to wait for.
        :param sync:
            If True, the beat interval will be synchronized
            to the start of the clock, returning an adjusted number
            of ticks to match that interval.
            If False, no synchronization is done and the returned
            number of ticks will always be the number of beats multiplied
            by the clock `ppqn`.
        :returns: The number of ticks needed to wait.

        """
        interval = int(self.ppqn * n_beats)
        if interval <= 0:
            return 0
        elif not sync:
            return interval

        return interval - self.tick % interval

    def get_bar_ticks(self, n_bars: Union[int, float], *, sync: bool = True) -> int:
        """Determines the number of ticks to wait for N bars to pass.

        :param n_bars: The number of bars to wait for.
        :param sync:
            If True, the ticks calculated for the first bar
            is reduced to synchronize with the clock.
        :returns: The number of ticks needed to wait.

        """
        interval = int(self.ppqn * self.beat_per_bar * n_bars)
        if interval <= 0:
            return 0
        elif not sync:
            return interval

        return interval - self.tick % interval

    def _get_tick_duration(self) -> float:
        """Determines the numbers of seconds the next tick will take.

        Only required when clock is running in active mode.

        """
        accel_mult = 1 - self.accel / 100
        nudge = self._nudge
        self._nudge = 0
        interval = 60 / self.bpm / self.ppqn * accel_mult
        result = (interval - self._delta) + nudge
        return result if result >= 0 else 0.0

    # TODO: increment_clock should handle 'tick' events

    def _increment_clock(self, temporal_information: Optional[dict]):
        """
        This method is in charge of increment the clock (moving forward
        in time). In normal MIDI Clock Mode, this is as simple as
        ticking forward (+1) and updating handles so they notice that
        change.

        If Link is activated, temporal information must be received in
        order to pinpoint the actual point of Link in time. This way,
        Sardine can move time in accord with that reference point, while
        trying to preserve its internal logic based on pulses per quarter
        notes.
        """
        if temporal_information:
            self._current_tick = self._link_time_to_ticks(temporal_information)
        else:
            self._current_tick += 1
        self._update_handles()

    def _reload_runners(self):
        for runner in self.runners.values():
            runner.reload()

    def _shift_handles(self, n_ticks: int):
        for handle in self.tick_handles:
            handle.when += n_ticks

    def _update_handles(self):
        # this is implemented very similarly to asyncio.BaseEventLoop
        while self.tick_handles:
            handle = self.tick_handles[0]
            if handle.cancelled():
                heapq.heappop(self.tick_handles)
            elif self.tick >= handle.when:
                handle.fut.set_result(None)
                heapq.heappop(self.tick_handles)
            else:
                # all handles afterwards are either still waiting or cancelled
                break

    # ---------------------------------------------------------------------- #
    # Scheduler methods

    def schedule_func(self, func: MaybeCoroFunc, /, *args, **kwargs):
        """Schedules the given function to be executed."""
        if not (inspect.isfunction(func) or inspect.ismethod(func)):
            raise TypeError(f"func must be a function, not {type(func).__name__}")

        name = func.__name__
        runner = self.runners.get(name)
        if runner is None:
            runner = self.runners[name] = AsyncRunner(
                clock=self, deferred=self.deferred_scheduling
            )

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

    def wait_until(self, *, tick: int) -> TickHandle:
        """Returns a TickHandle that waits for the clock to reach a certain tick."""
        handle = TickHandle(tick)

        # NOTE: we specifically don't want this influenced by `tick_shift`
        if self._current_tick >= tick:
            handle.fut.set_result(None)
        else:
            heapq.heappush(self.tick_handles, handle)

        return handle

    def wait_after(self, *, n_ticks: int) -> TickHandle:
        """Returns a TickHandle that waits for the clock to pass N ticks from now."""
        return self.wait_until(tick=self.tick + n_ticks)

    # ---------------------------------------------------------------------- #
    # Public methods

    def print_children(self):
        """Print all children on clock"""
        [print(child) for child in self.runners]

    def reset(self):
        for runner in self.runners.values():
            runner.stop()
        for handle in self.tick_handles:
            handle.cancel()

        self.runners.clear()
        self.tick_handles.clear()
