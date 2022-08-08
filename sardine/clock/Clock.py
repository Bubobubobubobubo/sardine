import asyncio
import contextvars
import functools
import heapq
import inspect
import time
from typing import Awaitable, Callable, Optional, TypeVar, Union
from collections import deque


import mido
from rich import print

from . import AsyncRunner
from ..io import MIDIIo, ClockListener
from ..superdirt import SuperDirt

__all__ = ('Clock', 'TickHandle')

T = TypeVar('T')
MaybeCoroFunc = Callable[..., Union[T, Awaitable[T]]]

tick_shift = contextvars.ContextVar('tick_shift', default=0)
"""
This specifies the number of ticks to offset the clock in the current context.

Usually this tick shift is updated within the context of scheduled functions
to simulate sleeping without actually blocking the function.
Behavior is undefined if the tick shift is changed in the global context.
"""


@functools.total_ordering
class TickHandle:
    """A handle that allows waiting for a specific tick to pass in the clock."""
    __slots__ = ('when', 'fut')


    def __init__(self, tick: int):
        self.when = tick
        self.fut = asyncio.Future()


    def __repr__(self):
        return '<{} {} when={}>'.format(
            type(self).__name__,
            'pending' if not self.fut.done()
            else 'done' if not self.fut.cancelled()
            else 'cancelled',
            self.when
        )

    def __eq__(self, other):
        if not isinstance(other, TickHandle):
            return NotImplemented
        return self.when == other.when and self.fut == other.fut

    def __hash__(self):
        return hash((self.when, self.fut))

    def __lt__(self, other):
        if not isinstance(other, TickHandle):
            return NotImplemented
        return self.when < other.when


    def __await__(self):
        return self.fut.__await__()


    def cancel(self):
        return self.fut.cancel()


    def cancelled(self):
        return self.fut.cancelled()


class Clock:

    """
    Naive MIDI Clock and scheduler implementation. This class
    is the core of Sardine. It generates an asynchronous MIDI
    clock and will schedule functions on it accordingly.

    Keyword arguments:
    port_name: str -- Exact String for the MIDIOut Port.
    bpm: Union[int, float] -- Clock Tempo in beats per minute
    beats_per_bar: int -- Number of beats in a given bar
    deferred_scheduling: bool -- Whether the clock implicitly defers
                                 sounds sent in functions or not.
    """

    def __init__(
        self,
        midi_port: Optional[str],
        ppqn: int = 48,
        bpm: Union[float, int] = 120,
        beats_per_bar: int = 4,
        deferred_scheduling: bool = True
    ):
        self._midi = MIDIIo(
                port_name=midi_port,
                clock=self)

        # Clock parameters
        self._accel = 0.0
        self._bpm = bpm
        self._ppqn = ppqn
        self.beat_per_bar = beats_per_bar
        self.running = False
        self.debug = False

        # Scheduling attributes
        self.runners: dict[str, AsyncRunner] = {}
        self.tick_handles: list[TickHandle] = []
        self._deferred_scheduling = deferred_scheduling

        # Real-time attributes
        self._current_tick = 0
        self._delta = 0.0

        # MIDI In Listener
        self._midi_port = midi_port
        self._listener = None
        self._delta_duration_list = deque(maxlen=200)

    def __repr__(self):
        shift = tick_shift.get()
        if shift:
            tick = f'{self._current_tick}{shift:+}'
        else:
            tick = str(self._current_tick)

        return '<{} running={} tick={}>'.format(
            type(self).__name__, self.running, tick
        )

    # ---------------------------------------------------------------------- #
    # Clock properties

    @property
    def accel(self) -> int:
        return self._accel

    @accel.setter
    def accel(self, value: int):
        if value >= 100:
            raise ValueError('cannot set accel above 100')
        self._accel = value
        self._reload_runners()

    @property
    def deferred_scheduling(self):
        return self._deferred_scheduling

    @deferred_scheduling.setter
    def deferred_scheduling(self, enabled: bool):
        self._deferred_scheduling = enabled

        for runner in self.runners.values():
            runner.deferred = enabled

    @property
    def tick(self) -> int:
        return self._current_tick + tick_shift.get()

    @tick.setter
    def tick(self, new_tick: int) -> int:
        change = new_tick - self._current_tick
        self._current_tick = new_tick
        self._shift_handles(change)
        self._reload_runners()
        self._update_handles()

    @property
    def bpm(self) -> int:
        return self._bpm

    @bpm.setter
    def bpm(self, new_bpm: int):
        if not 1 < new_bpm < 900:
            raise ValueError('bpm must be within 1 and 800')
        self._bpm = new_bpm
        self._reload_runners()

    @property
    def ppqn(self) -> int:
        return self._ppqn

    @ppqn.setter
    def ppqn(self, pulses_per_quarter_note: int) -> int:
        self._ppqn = pulses_per_quarter_note
        self._reload_runners()

    @property
    def current_beat(self) -> int:
        """The number of beats passed since the initial time."""
        return self.tick // self.ppqn

    @property
    def current_bar(self) -> int:
        """The number of bars passed since the initial time."""
        return self.current_beat // self.beat_per_bar

    @property
    def phase(self) -> int:
        """The phase of the current beat in ticks."""
        return self.tick % self.ppqn

    # ---------------------------------------------------------------------- #
    # Clock methods

    def get_beat_ticks(self, n_beats: Union[int, float], *, sync: bool = True) -> int:
        """Determines the number of ticks to wait for N beats to pass.

        :param n_beats: The number of beats to wait for.
        :param sync:
            If True, the ticks calculated for the first beat
            is reduced to synchronize with the clock.
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

    def shift_ctx(self, n_ticks: int):
        """Shifts the clock by `n_ticks` in the current context.

        This is useful for simulating sleeps without blocking.

        If the real-time clock tick needs to be shifted,
        assign to the `c.tick` property instead.

        """
        tick_shift.set(tick_shift.get() + n_ticks)

    def _get_tick_duration(self) -> float:
        """Determines the numbers of seconds the next tick will take.

        Only required when clock is running in active mode.

        """
        accel_mult = 1 - self.accel / 100
        interval = 60 / self.bpm / self.ppqn * accel_mult
        return interval - self._delta

    def _increment_clock(self):
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
        if not inspect.isfunction(func):
            raise TypeError(f'func must be a function, not {type(func).__name__}')

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
        """ Print all children on clock """
        [print(child) for child in self.runners]

    def start(self, active=True):
        """Start MIDI Clock"""
        self.reset()
        if not self.running:
            self._midi.send(mido.Message('start'))
            self.running = True
            if active:
                asyncio.create_task(self.run_active())
            else:
                asyncio.create_task(self.run_passive())

    def reset(self):
        for runner in self.runners.values():
            runner.stop()
        for handle in self.tick_handles:
            handle.cancel()

        self.runners.clear()
        self.tick_handles.clear()

    def stop(self) -> None:
        """
        MIDI Stop message.
        """
        # Kill every runner

        self.running = False
        self._midi.send_stop()
        self._midi.send(mido.Message('stop'))
        self.reset()

    def log(self) -> None:
        """
        Pretty print information about Clock timing on the console.
        Used for debugging purposes. Not to be used when playing,
        can be very verbose. Will overflow the console in no-time.
        """
        cbib = (self.current_beat % self.beat_per_bar) + 1
        bar = self.current_bar

        color = "[bold yellow]"
        first = color + f"BPM: {self.bpm}, PHASE: {self.phase:02}, DELTA: {self._delta:2f}"
        second = color + f" || TICK: {self.tick} BAR:{bar} {cbib}/{self.beat_per_bar}"
        print(first + second)


    def note(self, sound: str, at: int = 0, **kwargs) -> SuperDirt:
        return SuperDirt(self, sound, at, **kwargs)


    # def midinote(self, sound: str, at: int = 0, **kwargs) -> SuperDirt:
    #     return SuperDirt(self, sound, at, **kwargs)


    async def run_active(self):
        """Main runner for the active mode (master)"""
        self._current_tick = 0
        self._delta = 0.0

        while self.running:
            begin = time.perf_counter()

            duration = self._get_tick_duration()
            await asyncio.sleep(duration)
            self._midi.send_clock()
            self._increment_clock()

            elapsed = time.perf_counter() - begin
            self._delta = elapsed - duration

            if self.debug:
                self.log()

    def _estimate_bpm_from_delta(self, delta: float) -> float:
        """Estimate the current BPM from delta value"""
        quarter_duration = delta * self.ppqn
        return 60 / quarter_duration


    def _mean_from_delta(self):
        """Estimate the current BPM by doing an arithmetic mean"""
        return sum(self._delta_duration_list) / len(self._delta_duration_list)

    async def run_passive(self):
        """Main runner for the passive mode (slave)"""
        self._listener = ClockListener(port=self._midi_port)
        self._current_tick = 0
        self._delta = 0.0
        while self.running:
            begin = time.perf_counter()
            await asyncio.sleep(0.0)
            self._listener.wait_for_tick()
            self._increment_clock()
            elapsed = time.perf_counter() - begin
            self._delta_duration_list.append(
                    self._estimate_bpm_from_delta(elapsed))
            self._bpm = self._mean_from_delta()
            if self.debug:
                self.log()
