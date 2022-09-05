import asyncio
import contextvars
import functools
import heapq
import inspect
import time
from typing import Awaitable, Callable, Optional, TypeVar, Union
from collections import deque
from numba import jit

import mido
from rich import print

from sardine.io.Osc import Client

from . import AsyncRunner
from ..io import MIDIIo, ClockListener, SuperDirtSender, MIDISender, OSCSender

__all__ = ("Clock", "TickHandle")

T = TypeVar("T")
MaybeCoroFunc = Callable[..., Union[T, Awaitable[T]]]

# This specifies the number of ticks to offset the clock in the
# current context.  # Usually this tick shift is updated within
# the context of scheduled functions to simulate sleeping
# without actually blocking the function. Behavior is undefined
# if the tick shift is changed in the global context.
tick_shift = contextvars.ContextVar("tick_shift", default=0)


@functools.total_ordering
class TickHandle:
    """A handle that allows waiting for a specific tick to pass in the clock."""

    __slots__ = ("when", "fut")

    def __init__(self, tick: int):
        self.when = tick
        self.fut = asyncio.Future()

    def __repr__(self):
        return "<{} {} when={}>".format(
            type(self).__name__,
            "pending"
            if not self.fut.done()
            else "done"
            if not self.fut.cancelled()
            else "cancelled",
            self.when,
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
    MIDI Clock and scheduler implementation. This class is
    the core of Sardine. It generates an asynchronous MIDI
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
        deferred_scheduling: bool = True,
    ):
        self._midi = MIDIIo(port_name=midi_port, clock=self)
        self._osc = Client(
            ip="127.0.0.1", port=12345, name="SardineOsc", ahead_amount=0
        )
        self._link = None

        # Clock parameters
        self._accel: float = 0.0
        self._nudge: float = 0.0
        self._midi_nudge: float = 0.0
        self._superdirt_nudge: float = 0.0
        self._bpm: float = bpm
        self._ppqn: int = ppqn
        self.beat_per_bar: int = beats_per_bar
        self.running: bool = False
        self.debug: bool = False

        # Scheduling attributes
        self.runners: dict[str, AsyncRunner] = {}
        self.tick_handles: list[TickHandle] = []
        self._deferred_scheduling = deferred_scheduling

        # Real-time attributes
        self._current_tick = 0
        self._delta = 0.0
        self._phase_snapshot = 0

        # MIDI In Listener
        self._midi_port = midi_port
        self._listener = None
        self._delta_duration_list = deque(maxlen=200)

    def __repr__(self):
        shift = tick_shift.get()
        if shift:
            tick = f"{self._current_tick}{shift:+}"
        else:
            tick = str(self._current_tick)

        return "<{} running={} tick={}>".format(type(self).__name__, self.running, tick)

    # ---------------------------------------------------------------------- #
    # Clock properties

    @property
    def nudge(self) -> int:
        return self._nudge

    @nudge.setter
    def nudge(self, value: int):
        """Nudge the clock to align on another peer. Very similar to accel
        but temporary. Nudge will reset every time the clock loops around.

        Args:
            value (int): nudge factor
        """
        self._nudge = value
        self._reload_runners()

    @property
    def midi_nudge(self) -> int:
        return self._nudge

    @midi_nudge.setter
    def midi_nudge(self, value: int):
        """Nudge every MIDI Message by a given amount of time

        Args:
            value (int): nudge amount
        """
        self._midi_nudge = value

    @property
    def superdirt_nudge(self) -> int:
        return self._superdirt_nudge

    @superdirt_nudge.setter
    def superdirt_nudge(self, value: int):
        """Nudge every SuperDirt Message by a given amount of time.
        Beware, nudging in the clock through this attribute is not
        the same as nudging the OSC messages themselves. If you get
        late messages in SuperDirt, please configure ahead_amount for
        the OSC object.

        Args:
            value (int): nudge amount
        """
        self._superdirt_nudge = value

    @property
    def accel(self) -> int:
        return self._accel

    @accel.setter
    def accel(self, value: int):
        """Accel stands for acceleration. In active MIDI mode, accel acts as
        a way to nudge the clock to run faster or slower (from 0 to 100%). It
        can be quite useful when dealing with a musician that can't really use
        any synchronisation protocol.


        Args:
            value (int): a nudge factor from 0 to 100%

        Raises:
            ValueError: if 'value' exceeds 100%
        """
        if value >= 100:
            raise ValueError("Cannot set acceleration above 100%.")
        self._accel = value
        self._reload_runners()

    @property
    def deferred_scheduling(self):
        return self._deferred_scheduling

    @deferred_scheduling.setter
    def deferred_scheduling(self, enabled: bool):
        """Turn on deferred scheduling.

        Args:
            enabled (bool): True or False
        """
        self._deferred_scheduling = enabled

        for runner in self.runners.values():
            runner.deferred = enabled

    @property
    def tick(self) -> int:
        return self._current_tick + tick_shift.get()

    @tick.setter
    def tick(self, new_tick: int) -> int:
        """Tick is the tiniest amount of time tracked by Sardine
        Clock. A tick is the time taken by the clock to loop on
        itself. Ticks are used by the system to deduce all other
        temporal informations: beat, bar, etc...

        Args:
            new_tick (int): give a new tick (backwards or forward in time)
        """
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
        """Beats per minute. Tempo for the Sardine Clock.

        Args:
            new_bpm (int): new tempo value

        Raises:
            ValueError: if tempo < 20 or tempo > 999 (non-musical values)
        """
        if not 20 < new_bpm < 999:
            raise ValueError("bpm must be within 1 and 800")
        self._bpm = new_bpm
        if self._link:
            pass
        self._reload_runners()

    @property
    def ppqn(self) -> int:
        return self._ppqn

    @ppqn.setter
    def ppqn(self, pulses_per_quarter_note: int) -> int:
        """Pulse per quarter note: how many pulses to form a quarter
        note. Typically used by MIDI Clocks, the PPQN is an important
        value to determine how fast a clock will be ticking and counting
        beats, measures, etc... It is important to make sure that your PPQN
        is identic to the PPQN of the device you are trying to synchronise
        with.

        Args:
            pulses_per_quarter_note (int): Generally a multiple of 2 (24, 48).
        """
        self._ppqn = pulses_per_quarter_note
        self._reload_runners()

    @property
    def current_beat(self) -> int:
        """The number of beats passed since the initial time."""
        return self.tick // self.ppqn

    @property
    def beat(self) -> int:
        """The number of beats passed since the initial time."""
        return self.tick // self.ppqn

    @property
    def current_bar(self) -> int:
        """The number of bars passed since the initial time."""
        return self.current_beat // self.beat_per_bar

    @property
    def bar(self) -> int:
        """The number of bars passed since the initial time."""
        return self.current_beat // self.beat_per_bar

    @property
    def phase(self) -> int:
        """The phase of the current beat in ticks."""
        return self.tick % self.ppqn

    # ---------------------------------------------------------------------- #
    # Clock methods

    # ----------------------------------------------------------------------------------------
    # Link related functions

    def link(self):
        """
        Synchronise Sardine with Ableton Link. This method will call a new
        instance of link through the LinkPython package (pybind11). As soon
        as this instance is created, Sardine will instantly try to lock on
        the new timegrid and share tempo with Link peers.

        NOTE: the Ableton Link mechanism is currently unstable and should be
        used for test purposes only. You might end up loosing some events that
        are ready for scheduling in your swimming functions!
        """
        import link
        self._link = link.Link(self.bpm)
        self._link.enabled = True
        self._link.startStopSyncEnabled = True

        # We need to capture a first snapshot of time outside of the main
        # mechanism in order to start calculations somewhere...
        i = self._capture_link_info()
        self._phase_snapshot = int(abs(round(self._scale(
            i["phase"], (0, self.beat_per_bar),
            (0, self.ppqn * self.beat_per_bar))) % self.ppqn))

        print('[red bold]Joining Link Session: [/red bold]', end='')

    def unlink(self):
        """
        Close connexion to Ableton Link by deleting the object. Sardine will
        continue as if time never stopped ticking from the moment the clock
        was disconnected from Link Clock (ticks will continue to increase, as
        well as beat number). Tempo will not be updated to fall back to initial
        value.
        """
        del self._link
        self._link = None
        print('[red bold]Broke away from Link Session[/red bold]')

    def link_stop(self):
        """
        Ableton Link Method to stop the timeline
        """
        self._link.enabled = False

    @jit
    def _capture_link_info(self):
        """Capture information about the current state of the Ableton Link
        session. This internal method will try to gather high-res temporal
        informations for later processing.

        Returns:
            dict: a dictionnary containing temporal information about the Link
            session.
        """
        if self._link:
            s = self._link.captureSessionState()
            link_time = self._link.clock().micros()
            tempo_str = s.tempo()
            # beats_str = s.beatAtTime(link_time, self.beat_per_bar)
            beats_str = s.beatAtTime(link_time, self.beat_per_bar / 2)
            playing_str = str(s.isPlaying())
            phase = s.phaseAtTime(link_time, self.beat_per_bar)
            return {
                "tempo": tempo_str,
                "beats": beats_str,
                "playing": playing_str,
                "phase": phase,
            }

    def link_log(self):
        """Print state of current Ableton Link session on stdout."""
        i = self._capture_link_info()
        print(
            f'tempo {i["tempo"]} | playing {i["playing"]} | beats {i["beats"]} | phase {i["phase"]}'
        )

    @jit(fastmath=True)
    def _scale(
        self,
        x: Union[int, float],
        old: tuple[int, int],
        new: tuple[int, int]
    ):
        return (x - old[0]) * (new[1] - new[0]) / (old[1] - old[0]) + new[0]

    @jit
    def _link_phase_to_ppqn(self, captured_info: dict):
        """Convert Ableton Link phase (0 to quantum, aka number of beats)
        to Sardine phase (based on ticks and pulses per quarter notes).
        The conversion is done using the internal _scale subfunction.

        Returns:
            int: current phase (0 - self.ppqn)
        """
        new_phase = round(self._scale(
            captured_info["phase"],
            (0, self.beat_per_bar),
            (0, self.ppqn * self.beat_per_bar))) % self.ppqn

        # Whatever happens, we need to move forward
        if self._phase_snapshot == new_phase:
            new_phase += 1
        # But we can't tolerate phase discontinuities
        if new_phase == self._phase_snapshot + 2:
            new_phase -= 1

        self._phase_snapshot = new_phase
        return int(abs(self._phase_snapshot))

    @jit
    def _link_beat_to_sardine_beat(self, captured_info: dict):
        """Convert Ableton Link beats to valid Sardine beat"""
        return int(captured_info["beats"])

    @jit
    def _link_time_to_ticks(self, captured_info: dict):
        """Convert Ableton Link time to ticks, used by _increment_clock"""
        phase = int(self._link_phase_to_ppqn(captured_info))
        beat = int(captured_info["beats"]) * (self.ppqn)
        return beat + phase

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
        nudge = self._nudge
        self._nudge = 0
        interval = 60 / self.bpm / self.ppqn * accel_mult
        result = (interval - self._delta) + nudge
        return result if result >= 0 else 0.0

    @jit
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
        if self._link:
            if self.phase == 0:
                self.bpm = float(temporal_information["tempo"])
            self._current_tick = self._link_time_to_ticks(
                temporal_information)
            self._update_handles()
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
        if not inspect.isfunction(func):
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

    def start(self, active=True):
        """Start MIDI Clock"""
        self.reset()
        if not self.running:
            self._midi.send(mido.Message("start"))
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
        self._midi.send(mido.Message("stop"))
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
        first = (
            color + f"BPM: {self.bpm}, PHASE: {self.phase:02}, DELTA: {self._delta:2f}"
        )
        second = color + f" || TICK: {self.tick} BAR:{bar} {cbib}/{self.beat_per_bar}"
        print(first + second)

    def note(self, sound: str, at: int = 0, **kwargs) -> SuperDirtSender:
        return SuperDirtSender(self, sound, at, nudge=self._superdirt_nudge, **kwargs)

    def midinote(
        self,
        note: Union[int, str] = 60,
        velocity: Union[int, str] = 100,
        channel: Union[int, str] = 0,
        delay: Union[int, float, str] = 0.1,
        at: int = 0,
        **kwargs,
    ) -> MIDISender:
        return MIDISender(
            self,
            self._midi,
            at=at,
            delay=delay,
            note=note,
            velocity=velocity,
            channel=channel,
            nudge=self._midi_nudge,
            **kwargs,
        )

    def oscmessage(self, connexion, address: str, at: int = 0, **kwargs) -> OSCSender:
        return OSCSender(
            clock=self, osc_client=connexion, address=address, at=at, **kwargs
        )

    def _sardine_beat_to_link_beat(self):
        integer_part = self.beat + 1
        floating_part = self.phase / self.ppqn
        return float(integer_part + floating_part)

    async def run_active(self):
        """Main runner for the active mode (master)"""
        self._current_tick, self._delta = 0, 0.0

        while self.running:
            begin = time.perf_counter()
            duration = self._get_tick_duration()
            if self._link:
                fetch_begin = time.perf_counter()
                info = self._capture_link_info()
                fetch_end = time.perf_counter()
                sleep_duration = (fetch_end - fetch_begin) + duration
                if sleep_duration >= 0:
                    await asyncio.sleep(sleep_duration)
                else:
                    pass
                self._increment_clock(temporal_information=info)
            else:
                await asyncio.sleep(duration)
                self._midi.send_clock()
                self._osc._send_clock_information(self)
                # We can't tell if the user has switched to Link
                # in the meantime. You should be ready to send
                # link state whenever needed.
                self._increment_clock(
                    temporal_information=(self._capture_link_info(
                        ) if self._link else None))
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
            self._delta_duration_list.append(self._estimate_bpm_from_delta(elapsed))
            self._bpm = self._mean_from_delta()
            if self.debug:
                self.log()
