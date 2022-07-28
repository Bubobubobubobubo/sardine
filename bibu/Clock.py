import asyncio
import inspect
import uvloop
import itertools
import mido
import time
from rich import print
from typing import Union, List, Any, Callable, Awaitable
from math import floor
from concurrent.futures import ThreadPoolExecutor
import threading
from .Sound import Sound
from dataclasses import dataclass
from functools import wraps

"""
Nouveau problème : je ne comprends plus rien au BPM et à la durée des notes.
"""

@dataclass
class SyncRunner:
    function: Any
    delay: int
    kwargs: list


@dataclass
class AsyncRunner:
    function: Any
    delay: int
    kwargs: list


class MIDIIo(threading.Thread):

    """
    blabla
    """

    def __init__(self, port_name: str= None):
        threading.Thread.__init__(self)
        self._midi_ports = mido.get_output_names()
        if port_name:
            try:
                self._midi = mido.open_output()
            except Exception as error:
                print(f"[bold red]Init error: {error}[/bold red]")
        else:
            try:
                self._midi = mido.open_output(self._midi_ports[0])
            except Exception as error:
                print(f"[bold red]Init error: {error}[/bold red]")

    def send(self, message: mido.Message) -> None:
        self._midi.send(message)

    async def send_async(self, message: mido.Message) -> None:
        self._midi.send(message)

    def send_stop(self) -> None:
        """ MIDI Start message """
        self._midi.send(mido.Message('stop'))

    def send_reset(self) -> None:
        """ MIDI Reset message """
        self._midi.send(mido.Message('reset'))
        # self._reset_internal_clock_state()

    def send_clock(self) -> None:
        """ MIDI Clock Message """
        self._midi.send(mido.Message('clock'))

    async def send_clock_async(self) -> None:
        """ MIDI Clock Message """
        self._midi.send(mido.Message('clock'))


    async def send_start(self, initial: bool = False) -> None:
        """ MIDI Start message """
        self._midi.send(mido.Message('start'))


class Time:
    def __init__(self, ppqn: int, bar: Union[int, float] = 0,
                 beat: Union[int, float] = 0, phase: int = 0):

        """
        Generate a time target in the future. The function needs a PPQN
        to be used as reference. The PPQN will be used to decompose bars
        and beats in a given nb of PPQN to reach the target.

        ppqn: int -- How many PPQN are used by the system
        bar:  Union[int, float]  -- How many bars in the future
        beat: Union[int, float]  -- How many beats in the future
        phase: Union[int, float] -- How many PPQN in the future
        """

        self.ppqn = ppqn
        bar_standard, beat_standard = ppqn * 4, ppqn
        self.bar = floor(bar_standard * bar)
        self.beat = floor(beat_standard * beat)
        self.phase = phase

    def target(self) -> int:
        """ Return the number of PPQN to reach target """
        return self.beat + self.bar + self.phase

    def __sub__(self, other):
        """ Substraction between a time and another time """
        print(f"A: {self.bar} {self.beat} {self.phase}")
        print(f"B: {other.bar} {other.beat} {other.phase}")
        print(f"C: {self.bar - other.bar} {self.beat - other.beat} {self.phase - other.phase}")


class Clock:

    """
    Very naive MIDI Clock. Lots of jitter and time problems.
    The reason is that everything, including blocking I/O is
    still running in the same thread.

    Keyword arguments:
    port_name: str -- Exact String for the MIDIOut Port.
    bpm: Union[int, float] -- Clock Tempo in beats per minute
    beats_per_bar: int -- Number of beats in a given bar
    """

    def __init__(self, port_name: str,
                 bpm: Union[float, int] = 120,
                 beat_per_bar: int = 4):

        self._midi = MIDIIo()

        # Clock maintenance related
        self.child = {}

        self.running = False
        self._debug = False
        # Timing related
        self._bpm = bpm
        self.initial_time = 0
        self.delta = 0
        self.beat = -1
        self.ppqn = 12
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

    def __rshift__(self, coroutine):
        """ Add a new task to the scheduler """
        asyncio.create_task(coroutine)
    
    def _auto_schedule(self, function, delay, **kwargs):
        asyncio.create_task(self._schedule(
                function=function,
                delay=delay,
                **kwargs))

    def schedule(self, function, delay, **kwargs):

        """
        Outer layer of the schedule function. Deals with registering.
        Two types of functions can be scheduled: sync and async funcs.
        They should not be scheduled the same because async functions
        can handle time on their own.

        SyncRunner -- a synchronous runner. Before start, the function
        should be transformed into an async runner but it will still be
        identified as a synchronous runner because it has been wrapped.

        AsyncRunner -- an asynchronous runner. The function will start
        immediately but should be able to reschedule itself with a call
        back once it comes back.

        TODO: Fix tempo stuff

        """

        def to_coroutine(f: Callable[..., Any]):
            """ turn function into async func """
            @wraps(f)
            async def wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapper

        def force_awaitable(
                function: Union[Callable[..., Awaitable[Any]], Callable[..., Any]]
                ) -> Callable[..., Awaitable[Any]]:
            """ force function to be awaitable """
            if inspect.iscoroutinefunction(function):
                return function
            else:
                return to_coroutine(function)

        if function.__name__ in self.child.keys():
            # For asynchronous functions
            if inspect.iscoroutinefunction(function):
                self.child[function.__name__].function = function
            # For synchronous functions
            else:
                self.child[function.__name__].function = (
                        force_awaitable(function))
            self.child[function.__name__].delay = delay
            self.child[function.__name__].kwagrgs = kwargs
            return

        else:
            # For asynchronous functions
            if inspect.iscoroutinefunction(function):
                self.child[function.__name__] = AsyncRunner(
                        function=function, delay=delay, kwargs=kwargs)

            # For synchronous functions
            else:
                self.child[function.__name__] = SyncRunner(
                        function=force_awaitable(function),
                        delay=delay, kwargs=kwargs)

            asyncio.create_task(
                    self._schedule(
                        function=self.child[function.__name__].function,
                        delay=self.child[function.__name__].delay,
                        init=True,
                        **self.child[function.__name__].kwargs))

    def remove(self, function):
        """ Remove a function from the scheduler """
        if function.__name__ in self.child.keys():
            del self.child[function.__name__]


    async def _schedule(self, function, delay, init=False, **kwargs):
        """ Inner scheduling """

        if init:
            while self.phase != 1:
                await asyncio.sleep(self._get_tick_duration())

        # Busy waiting until execution time
        now = self.get_tick_time()
        target_time = ((now + delay) - self.tick_time) * self._get_tick_duration()
        await asyncio.sleep(target_time - 5)
        while self.tick_time < now + delay:
            await asyncio.sleep(self._get_tick_duration())

        # Execution time
        if function.__name__ in self.child.keys():
            asyncio.create_task(
                    self.child[function.__name__].function(
                        **self.child[function.__name__].kwargs))

        # Rescheduling time
            self._auto_schedule(
                function=self.child[function.__name__].function,
                delay=self.child[function.__name__].delay,
                init=False,
                **self.child[function.__name__].kwargs)

    # ---------------------------------------------------------------------- #
    # Public methods

    def print_children(self):
        """ Print all children on clock """
        [print(child) for child in self.child]

    def ticks_to_next_bar(self) -> None:
        """ How many ticks until next bar? """
        return (self.ppqn - self.phase - 1) * self._get_tick_duration()

    async def play_note(self, note: int = 60, channel: int = 0,
                        velocity: int = 127,
                        duration: Union[float, int] = 1) -> None:

        """
        Dumb method that will play a note for a given duration.
        Here for test purposes.
        This function might introduce some latency because it 
        relies on IO. I should try to do something to speed it
        up.
        
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

        color = "[bold yellow]"
        beat, bar, delta, phase = (self.beat, self.elapsed_bars,
                                   self.delta, self.phase)
        print(color + f"BPM:{self._bpm} @{beat} Bar: {bar} Delta: {delta:2f} Phase: {phase}")
        print(color + f" Current: {self.current_beat}/{self.beat_per_bar}")


    async def run_clock(self):

        """
        Naive MIDI clock implementation. Drift will happen
        because of IO and miscalculations of time and will
        not be corrected.

        TODO: do better!

        Keyword arguments:
        debug: bool -- print debug messages on stdout.
        """

        async def _clock_update():
            """ Things the clock should do every tick """
            self._tick_duration = self._get_tick_duration()
            begin = time.perf_counter()
            self.delta = 0
            begin = time.perf_counter()
            end = time.perf_counter()
            self.delta = end - begin
            self.tick_duration = self._get_tick_duration()
            self.delta = 0  # reset delta
            await asyncio.sleep(self.tick_duration)
            asyncio.create_task(self._midi.send_clock_async())
            self.beat += 1
            self.tick_time += 1
            self._update_phase()
            if self.phase == 1:
                self._update_current_beat()
            if self.beat % self.ppqn == 0:
                self.elapsed_bars += 1
            end = time.perf_counter()
            self.delta = end - begin
            if self._debug:
                self.log()

        print(f"[bold red]Start clock with port {self._midi._midi_ports[0]}")
        while self.running:
            await _clock_update()

    def get_tick_time(self):
        """ Indirection to get tick time """
        return self.tick_time

    async def play(self, beat: int, note: int):
        """
        Test by playing a note on a given beat.

        beat: int -- targetted beat in the bar.
        note: int -- MIDI note to be played.
        """
        if self.current_beat == beat:
            asyncio.create_task(self.play_note(notej))

        self.__rshift__(self.play(beat, note))

    async def play_target(self, name: str, cur_time: int,
                          target: Union[Time, int],  note: int):
        """ Play a note in the future at given Time target """

        i_or_t = target.target() if isinstance(target, Time) else target
        t_until_t = ((cur_time + i_or_t) - self.tick_time) * self._get_tick_duration()
        await asyncio.sleep(t_until_t - 20)
        while self.tick_time < cur_time + i_or_t:
            await asyncio.sleep(self._get_tick_duration())
        asyncio.create_task(self.play_note(note))
 
        self.__rshift__(self.play_target(
            name=name, cur_time=clock.get_tick_time(),
            target=target, note=note))
