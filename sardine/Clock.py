import asyncio
import itertools
import mido
import time
from rich import print
from rich.console import Console
from typing import Union, Any
from math import floor
import threading
from dataclasses import dataclass


@dataclass
class AsyncRunner:
    function: Any
    tasks: list[Any, ...]


class MIDIIo(threading.Thread):

    """
    Direct MIDI I/O Using Mido. MIDI is also available indirectly
    through SuperDirt. I need to do something to address the redun-
    dancy.
    """

    def __init__(self, port_name: Union[str, None] = None):
        threading.Thread.__init__(self)
        self._midi_ports = mido.get_output_names()
        if port_name:
            try:
                self._midi = mido.open_output(port_name)
            except Exception as error:
                print(f"[bold red]Init error: {error}[/bold red]")
        else:
            try:
                self._midi = mido.open_output(self.choose_midi_port())
            except Exception as error:
                print(f"[bold red]Init error: {error}[/bold red]")

    def choose_midi_port(self) -> str:
        """ ASCII MIDI Port chooser """
        ports = mido.get_output_names()
        console = Console()
        for (i, item) in enumerate(ports, start=1):
            print(f"[color({i})] [{i}] {item}")
        nb = console.input("[bold yellow] Choose a MIDI Port: [/bold yellow]")
        try:
            nb = int(nb) - 1
            print(f'[yellow]You picked[/yellow] [green]{ports[nb]}[/green].')
            return ports[nb]
        except Exception:
            print(f"Input can only take valid number in range, not {nb}.")
            exit()

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
        OBSOLETE // DO NOT USE THIS CLASS

        Generate a time target in the future. The function needs
        a PPQN to be used as reference. The PPQN will be used to
        decompose bars and beats in a given nb of PPQN to reach the
        target.

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

        if function.__name__ in self.child.keys():
            self.child[function.__name__].function = function
            return

        else:
            self.child[function.__name__] = AsyncRunner(function=function)
            asyncio.create_task(
                    self._schedule(
                        function=self.child[function.__name__].function,
                        init=True))

    async def _schedule(self, function, init=False):
        """ Inner scheduling """

        def grab_arguments_from_coroutine(cr):
            """ Grab arguments from coroutine frame """
            arguments = cr.cr_frame
            arguments = arguments.f_locals
            return arguments

        arguments = grab_arguments_from_coroutine(function)
        delay = arguments["delay"]

        if init:
            while self.phase != 1:
                await asyncio.sleep(self._get_tick_duration())

        # Busy waiting until execution time
        now = self.get_tick_time()
        target_time = ((now + delay) - self.tick_time) * self._get_tick_duration()
        await asyncio.sleep(target_time - 10) # what is this magic number?
        while self.tick_time < now + delay:
            await asyncio.sleep(self._get_tick_duration())

        # Execution time
        if function.__name__ in self.child.keys():
            asyncio.create_task(self.child[function.__name__].function)

    def _auto_schedule(self, function):
        """ Loop mechanism """

        if function.__name__ in self.child.keys():
            self.child[function.__name__].function = function

            asyncio.create_task(self._schedule(
                function=self.child[function.__name__].function))

    def __rshift__(self, function):
        """ Alias to _auto_schedule """
        print(f"Func: {function.__name__}")
        print(f"{type(function)}")
        self._auto_schedule(function=function)

    def __lshift__(self, function):
        """ Alias to remove """
        self.remove(function=function)

    # ---------------------------------------------------------------------- #
    # Public methods

    def remove(self, function):
        """ Remove a function from the scheduler """
        if function.__name__ in self.child.keys():
            # Trying to cancel something here
            self.child[function.__name__].function.cancel()
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

        color = "[bold yellow]"
        beat, bar, delta, phase = (self.beat, self.elapsed_bars,
                                   self.delta, self.phase)
        print(color + f"BPM:{self._bpm} @{beat} Bar: {bar} Delta: {delta:2f} Phase: {phase}")
        print(color + f" Current: {self.current_beat}/{self.beat_per_bar}")


    async def run_clock(self):

        """
        Main Method for the MIDI Clock. Full of errors and things that
        msut be fixed. Drift can happen, and it might need a full rewrite.

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
            # end = time.perf_counter()
            # self.delta = end - begin
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

        while self.running:
            await _clock_update()

    def get_tick_time(self):
        """ Indirection to get tick time """
        return self.tick_time
