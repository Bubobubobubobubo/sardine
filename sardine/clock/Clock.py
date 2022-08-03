import asyncio
import functools
import heapq
import inspect
import mido
from rich import print
import time
from typing import Awaitable, Callable, Optional, Union

from .AsyncRunner import AsyncRunner
from ..io.MidiIo import MIDIIo
from ..superdirt.SuperDirt import SuperDirt


@functools.total_ordering
class TickHandle:
    """A handle that allows waiting for a specific tick to pass in the clock."""
    def __init__(self, tick: int):
        self.when = tick
        self.fut = asyncio.Future()

    def __eq__(self, other):
        if not isinstance(other, TickHandle):
            return NotImplemented
        return self.when == other.when and self.fut == other.fut

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
    """

    def __init__(
        self,
        midi_port: Optional[str],
        bpm: Union[float, int] = 120,
        beat_per_bar: int = 4
    ):
        self._midi = MIDIIo(port_name=midi_port)

        # Clock parameters
        self.bpm = bpm
        self.ppqn = 48
        self.beat_per_bar = beat_per_bar
        self.accel = 0.0
        self.running = False
        self.debug = False

        # Scheduling attributes
        self.runners: dict[str, AsyncRunner] = {}
        self.tick_handles: list[TickHandle] = []

        # Real-time attributes
        self._current_tick = 0
        self._delta = 0.0

        # MIDI In Listener
        self._listener = None

    def __repr__(self):
        return '<{} running={} tick={}>'.format(
            type(self).__name__, self.running, self._current_tick
        )

    # ---------------------------------------------------------------------- #
    # Clock properties

    @property
    def bpm(self) -> int:
        return self._bpm

    @bpm.setter
    def bpm(self, new_bpm: int):
        if not 1 < new_bpm < 800:
            raise ValueError('bpm must be within 1 and 800')
        self._bpm = new_bpm

    @property
    def current_beat(self) -> int:
        """The number of beats passed since the initial time."""
        return self._current_tick // self.ppqn

    @property
    def current_bar(self) -> int:
        """The number of bars passed since the initial time."""
        return self.current_beat // self.beat_per_bar

    @property
    def phase(self) -> int:
        """The phase of the current beat in ticks."""
        return self._current_tick % self.ppqn

    # ---------------------------------------------------------------------- #
    # Clock methods

    def get_beat_ticks(self, n_beats: Union[int, float]) -> int:
        """Returns the number of ticks to wait for N beats to pass."""
        interval = int(self.ppqn * n_beats)
        return interval - self._current_tick % interval

    def get_bar_ticks(self, n_bars: Union[int, float]) -> int:
        """Returns the number of ticks to wait for N bars to pass."""
        interval = int(self.ppqn * self.beat_per_bar * n_bars)
        return interval - self._current_tick % interval

    def _get_tick_duration(self) -> float:
        """Returns the numbers of seconds the next tick will take.

        Only required when clock is running in active mode.

        """
        accel = 1 - self.accel / 100
        interval = 60 / self.bpm / self.ppqn * accel
        return interval - self._delta

    def _increment_clock(self):
        # this is implemented very similarly to asyncio.BaseEventLoop
        self._current_tick = tick = self._current_tick + 1

        while self.tick_handles:
            handle = self.tick_handles[0]
            if handle.cancelled():
                heapq.heappop(self.tick_handles)
            elif tick >= handle.when:
                handle.fut.set_result(None)
                heapq.heappop(self.tick_handles)
            # all handles afterwards are either still waiting or cancelled
            break

    def ramp(self, min: int, max: int):
        """ Generate a ramp between min and max using phase """
        return self.phase % (max - min + 1) + min

    def iramp(self, min: int, max: int):
        """ Generate an inverted ramp between min and max using phase"""
        return self.ppqn - self.phase % (max - min + 1) + min

    # ---------------------------------------------------------------------- #
    # Scheduler methods

    def schedule_func(self, func: Callable, /, *args, **kwargs):
        """Schedules the given function to be executed."""
        if not inspect.isfunction(func):
            raise TypeError(f'func must be a coroutine function, not {type(func).__name__}')

        if self.running:
            name = func.__name__
            runner = self.runners.get(name)
            if runner is None:
                runner = self.runners[name] = AsyncRunner(self)

            runner.push(func, *args, **kwargs)
            if runner.started():
                runner.swim()
            else:
                runner.start()
        else:
            print(f"[red]Can't start {func.__name__} in absence of running clock.")

    def remove(self, func: Callable, /):
        """Schedules the given function to stop execution."""
        runner = self.runners[func.__name__]
        runner.stop()

    def wait_until(self, *, tick: int) -> Awaitable[None]:
        """Returns a TickHandle that waits for the clock to reach a certain tick."""
        handle = TickHandle(tick)
        heapq.heappush(self.tick_handles, handle)
        return handle

    def wait_after(self, *, n_ticks: int) -> Awaitable[None]:
        """Returns a TickHandle that waits for the clock to pass N ticks from now."""
        return self.wait_until(tick=self._current_tick + n_ticks)

    # ---------------------------------------------------------------------- #
    # Public methods

    def print_children(self):
        """ Print all children on clock """
        [print(child) for child in self.runners]

    def start(self):
        """ Restart message """
        self.reset()
        if not self.running:
            self._midi.send(mido.Message('start'))
            self.running = True
            asyncio.create_task(self.run_active())

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
        # Kill every runner

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

        color = "[bold red]" if self.phase == 1 else "[bold yellow]"
        first = color + f"BPM: {self.bpm}, PHASE: {self.phase:02}, DELTA: {self._delta:2f}"
        second = color + f" || [{self.tick_time}] {self.current_beat}/{self.beat_per_bar}"
        print(first + second)

    def note(self, sound: str, at: int = 0, **kwargs) -> SuperDirt:
        return SuperDirt(self, sound, at, **kwargs)

    async def run_active(self):
        """
        Main runner for the active mode (master)
        """
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

    async def run_passive(self):
        """
        Main runner for the passive mode (slave)
        """
        # on clock signal, increment internal counter
