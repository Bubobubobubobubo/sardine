import asyncio
import itertools
import mido
import time
from rich import print
from typing import Union
import traceback
from .AsyncRunner import AsyncRunner
from ..io.MidiIo import MIDIIo

atask = asyncio.create_task
sleep = asyncio.sleep

async def safe(coro, *args, **kwargs):
    while True:
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            # don't interfere with cancellations
            raise
        except Exception:
            print("a"*99999)
            exit()
            print("Caught exception")
            traceback.print_exc()


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
        self.child = {}

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

    def schedule(self, function):

        """
        Outer layer of the schedule function. Deals with registering.
        Two types of functions can be scheduled: sync and async funcs.
        They should not be scheduled the same because async functions
        can handle time on their own.

        AsyncRunner -- an asynchronous runner. The function will start
        immediately but should be able to reschedule itself with a call
        back once it comes back.

        The next step is to support argument passing to next iteration
        through keyword arguments!
        """
        name = function.__name__
        keys = self.child.keys()

        if name in keys:
            self.child[name].function = function
            return

        else:
            self.child[name] = AsyncRunner(
                    function=function,
                    last_valid_function=function,
                    tasks=[])

            self.child[name].tasks.append(atask(self._schedule(
                function=self.child[name].function,
                init=True)))

    async def _schedule(self, function, init=False):
        """ Inner scheduling """
        name = function.__name__
        cur_bar = self.elapsed_bars

        def grab_arguments_from_coroutine(cr):
            """ Grab arguments from coroutine frame """
            arguments = cr.cr_frame
            arguments = arguments.f_locals
            return arguments

        # Grab the `d` argument. Prevent a function from not having a `d`
        # argument! It will default to 1*self.ppqn
        arguments = grab_arguments_from_coroutine(function)
        try:
            delay = arguments["d"]
        except KeyError:
            delay = 1

        # Transform delay into multiple or division of ppqn
        delay = self.ppqn * delay

        if init:
            print(f"[Init {name}]")
            while (self.phase != 1 and self.elapsed_bars != cur_bar + 1):
                await sleep(self._get_tick_duration())
        else:
            # Busy waiting until execution time
            now = self.get_tick_time()
            while self.tick_time < now + delay:
                # You might increase the resolution even more
                await sleep(self._get_tick_duration() / self.ppqn)

        # Execution time
        # Trying something here with safe!
        if name in self.child.keys():
            self.child[name].tasks.append(
                safe(atask(self.child[name].function)))


    def _auto_schedule(self, function):
        """ Loop mechanism """

        # If the code reaches this point, first loop was succesful. It's time
        # to register a new version of last_valid_function. However, I need
        # to find a way to catch exceptions right here! Only Task exceptions
        # will show me if a task failed for some reason.
        name = function.__name__

        if name in self.child.keys():
            self.child[name].function = function
            self.child[name].tasks.append(
                asyncio.create_task(self._schedule(
                    function=self.child[name].function)))

    def __rshift__(self, function):
        """ Alias to _auto_schedule """
        self._auto_schedule(function=function)

    def __lshift__(self, function):
        """ Alias to remove """
        self.remove(function=function)

    # ---------------------------------------------------------------------- #
    # Public methods

    def remove(self, function):
        """ Remove a function from the scheduler """

        if function.__name__ in self.child.keys():
            del self.child[function.__name__]

    def get_phase(self):
        return self.phase

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
