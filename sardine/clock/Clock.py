import asyncio
from dataclasses import dataclass
import inspect
import itertools
import mido
from rich import print
import time
import traceback
from typing import Callable, Coroutine, Union
from ..io.MidiIo import MIDIIo


# Aliases
atask = asyncio.create_task
sleep = asyncio.sleep
CoroFunc = Callable[..., Coroutine]


@dataclass
class AsyncRunner:
    """Stores the arguments required to call the `Clock._runner()` method."""
    func: Callable
    args: tuple
    kwargs: dict


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

    def __init__(self, port_name: Union[str, None] = None,
                 bpm: Union[float, int] = 120,
                 beat_per_bar: int = 4):

        self._midi = MIDIIo(port_name=port_name)

        # Clock maintenance related
        self.func_runners: dict[str, list[AsyncRunner]] = {}

        self.running = False
        self._debug = False
        # Timing related
        self._bpm = bpm
        self.initial_time = 0
        self.delta = 0
        self.beat = -1
        self.ppqn = 48
        self._phase_gen = itertools.cycle(range(1, self.ppqn + 1))
        self.phase = 0
        self.beat_per_bar = beat_per_bar
        self._current_beat_gen = itertools.cycle(
                range(1, self.beat_per_bar + 1))
        self.current_beat = 0
        self.elapsed_bars = 0
        self.tick_duration = self._get_tick_duration()
        self.tick_time = 0

    # ---------------------------------------------------------------------- #
    # Setters and getters

    def get_bpm(self):
        """ BPM Getter """
        return self._bpm

    def set_bpm(self, new_bpm: int) -> None:
        """ BPM Setter """
        if 1 < new_bpm < 800:
            self._bpm = new_bpm
            self.tick_duration = self._get_tick_duration()

    def get_debug(self):
        """ Debug getter """
        return self._debug

    def set_debug(self, boolean: bool):
        """ Debug setter """
        self._debug = boolean

    bpm = property(get_bpm, set_bpm)
    debug = property(get_debug, set_debug)

    # ---------------------------------------------------------------------- #
    # Private methods

    def _get_tick_duration(self):
        return ((60 / self.bpm) / self.ppqn) - self.delta

    def _reset_internal_clock_state(self):
        """ Reset internal clock state with MIDI message """
        self.beat = -1
        self._phase_gen, self.phase = itertools.cycle(
                range(1, self.ppqn + 1)), 0
        self._current_beat_gen, self.current_beat = itertools.cycle(
                range(1, self.beat_per_bar)), 0
        self.elapsed_bars = 0
        self.tick_duration = ((self.bpm / 60) / self.beat_per_bar)

    def _update_phase(self) -> None:
        """ Update the current phase in MIDI Clock """
        self.phase = next(self._phase_gen)

    def _update_current_beat(self) -> None:
        """ Update the current beat in bar """
        self.current_beat = next(self._current_beat_gen)

    # ---------------------------------------------------------------------- #
    # Scheduler methods

    def schedule(self, func: CoroFunc, *args, **kwargs):
        """Schedules the given function to be executed."""
        if not inspect.iscoroutinefunction(func):
            raise TypeError(f'func must be a coroutine function, not {type(func).__name__}')

        name = func.__name__
        runners = self.func_runners.get(name)

        if runners is None:
            runners = self.func_runners[name] = []

        initial = False

        if not runners or func is not runners[-1].func:
            # initialize with new runner
            runner = AsyncRunner(func, args, kwargs)
            runners.append(runner)
            initial = True
        else:
            # update the top-most runner with new arguments
            runner = runners[-1]
            runner.args = args
            runner.kwargs = kwargs

        atask(self._runner(func, *args, initial=initial, **kwargs))

    async def _runner(self, func, *args, initial: bool, **kwargs):
        name = func.__name__
        cur_bar = self.elapsed_bars

        delay = kwargs.get('delay', 1)
        delay = delay * self.ppqn


        if initial:
            print(f"[Init {name}]")
            while (self.phase != 1 and self.elapsed_bars != cur_bar + 1):
                await sleep(self._get_tick_duration() / (self.ppqn * 2))
        else:
            # Busy waiting until execution time
            next_time = self.get_tick_time() + delay
            while self.tick_time < next_time:
                # You might increase the resolution even more
                await sleep(self._get_tick_duration() / (self.ppqn * 2))

        try:
            await func(*args, **kwargs)
        except asyncio.CancelledError:
            # assume the user has intentionally cancelled and ignore
            return
        except Exception as e:
            print(f'Exception encountered in {name}:')
            traceback.print_exception(e)
            self._reschedule(func)

    def _reschedule(self, func: CoroFunc):
        """
        Removes the previous AsyncRunner instance for a given function
        and dispatches any AsyncRunner before it, if it exists.
        """
        # pre: runners is not empty
        runners = self.func_runners[func.__name__]
        runners.pop()

        if not runners:
            return

        # reschedule the previous function invoked
        r = runners[-1]

        # patch the global scope so recursive functions don't
        # invoke the failed function
        func.__globals__[func.__name__] = r.func

        atask(self._runner(r.func, r.args, r.kwargs))


    # ---------------------------------------------------------------------- #
    # Public methods

    def remove(self, function: CoroFunc):
        """ Remove a function from the scheduler """
        self.func_runners.pop(function.__name__)

    def get_phase(self):
        return self.phase

    def print_children(self):
        """ Print all children on clock """
        [print(child) for child in self.func_runners]

    def ticks_to_next_bar(self) -> None:
        """ How many ticks until next bar? """
        return (self.ppqn - self.phase - 1) * self._get_tick_duration()

    async def play_note(self, note: int = 60, channel: int = 0,
                        velocity: int = 127,
                        duration: Union[float, int] = 1) -> None:

        """
        OBSOLETE // Was used to test things but should be removed.
        Dumb method that will play a note for a given duration.

        Keyword arguments:
        note: int -- the MIDI note to be played (default 1.0)
        duration: Union [int, float] -- MIDI tick time multiplier (default 1.0)
        channel: int -- MIDI Channel (default 0)
        velocity: int -- MIDI velocity (default 127)
        """

        async def send_something(message):
            """ inner non blocking function """
            asyncio.create_task(self._midi.send_async(message))

        note_on = mido.Message('note_on', note=note, channel=channel, velocity=velocity)
        note_off = mido.Message('note_off', note=note, channel=channel, velocity=velocity)
        await send_something(note_on)
        await asyncio.sleep(self.tick_duration * duration)
        await send_something(note_off)

    async def run_clock_initial(self):
        """ The MIDIClock needs to start """
        self.run_clock()

    def send_stop(self):
        """ Stop the running clock and send stop message """
        self.running = False
        self._midi.send_stop()

    def send_reset(self) -> None:
        """ MIDI Reset message """
        self.send_stop()
        self._midi.send(mido.Message('reset'))
        self._reset_internal_clock_state()

    async def send_start(self, initial: bool = False) -> None:
        """ MIDI Start message """
        self._midi.send(mido.Message('start'))
        self.running = True
        if initial:
            asyncio.create_task(self.run_clock())

    def next_beat_absolute(self):
        """ Return time between now and next beat in absolute time """
        return self.tick_duration * (self.ppqn - self.phase)

    def log(self) -> None:

        """
        Pretty print information about Clock timing on the console.
        Used for debugging purposes. Not to be used when playing,
        can be very verbose. Will overflow the console in no-time.
        """

        color = "[bold red]" if self.phase == 1 else "[bold yellow]"
        first = color + f"BPM: {self.bpm}, PHASE: {self.phase:02}, DELTA: {self.delta:2f}"
        second = color + f" || [{self.tick_time}] {self.current_beat}/{self.beat_per_bar}"
        print(first + second)


    async def run_clock(self):

        """
        Main Method for the MIDI Clock. Full of errors and things that
        msut be fixed. Drift can happen, and it might need a full rewrite.

        Keyword arguments:
        debug: bool -- print debug messages on stdout.
        """

        async def _clock_update():
            """ Things the clock should do every tick """

            self.tick_duration = self._get_tick_duration() - self.delta

            begin = time.perf_counter()
            self.delta = 0

            await asyncio.sleep(self.tick_duration)
            asyncio.create_task(self._midi.send_clock_async())

            # Time grains
            self.tick_time += 1
            self._update_phase()

            # XPPQN = 1 Beat
            if self.phase == 1:
                self._update_current_beat()
            if self.phase == 1 and self.current_beat == 1:
                self.elapsed_bars += 1

            # End of it
            end = time.perf_counter()
            self.delta = end - begin
            if self._debug:
                self.log()

        while self.running:
            await _clock_update()

    def get_tick_time(self):
        """ Indirection to get tick time """
        return self.tick_time

    def ramp(self, min: int, max: int):
        """ Generate a ramp between min and max using phase """
        return self.phase % (max - min + 1) + min

    def iramp(self, min: int, max: int):
        """ Generate an inverted ramp between min and max using phase"""
        return self.ppqn - self.phase % (max - min + 1) + min
