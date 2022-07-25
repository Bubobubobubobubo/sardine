import asyncio
import uvloop
import itertools
import mido
import time
from rich import print
from typing import Union
from math import floor
from concurrent.futures import ThreadPoolExecutor
import threading


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

    def send_stop(self) -> None:
        """ MIDI Start message """
        self._midi.send(mido.Message('stop'))

    def send_reset(self) -> None:
        """ MIDI Reset message """
        self._midi.send(mido.Message('reset'))
        self._reset_internal_clock_state()

    def send_clock(self) -> None:
        """ MIDI Clock Message """
        self._midi.send(mido.Message('clock'))

    def send_start(self, initial: bool = False) -> None:
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
                 bpm: Union[float, int] = 250,
                 beat_per_bar: int = 4):

        self._midi = MIDIIo()
        self._pool = ThreadPoolExecutor(max_workers=32)

        # Clock maintenance related
        self.tasks = {}

        self.running = True
        self._debug = False
        # Timing related
        self._bpm = bpm
        self.delta = 0
        self.beat = -1
        self.ppqn = 24
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
        self.tasks[coroutine.__qualname__] = asyncio.create_task(coroutine)

    def __lshift__(self, coroutine):
        """ Remove a task from the scheuler """
        del self.tasks[coroutine.__qualname__]

    # ---------------------------------------------------------------------- #
    # Public methods

    async def play_note(self, note: int = 60, channel: int = 0,
                        velocity: int = 127,
                        duration: Union[float, int] = 1) -> None:
        """
        Dumb method that will play a note for a given duration.
        
        Keyword arguments:
        note: int -- the MIDI note to be played (default 1.0)
        duration: Union [int, float] -- MIDI tick time multiplier (default 1.0)
        channel: int -- MIDI Channel (default 0)
        velocity: int -- MIDI velocity (default 127)
        """

        note_on = mido.Message('note_on', note=note, channel=channel, velocity=velocity)
        note_off = mido.Message('note_off', note=note, channel=channel, velocity=velocity)
        self._midi.send(note_on)
        await asyncio.sleep(self.tick_duration * duration)
        self._midi.send(note_off)

    async def run_clock_initial(self):
        """ The MIDIClock needs to start """
        self.run_clock()

    async def send_start(self, initial: bool = False) -> None:
        """ MIDI Start message """
        self._midi.send_start()
        self._midi.send(mido.Message('start'))
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

        print(f"[bold red]Start clock with port {self._midi._midi_ports[0]}")
        while self.running:
            self.tick_duration = self._get_tick_duration()
            self.delta = 0 # reset delta
            begin = time.perf_counter()
            await asyncio.sleep(self.tick_duration)
            self._midi.send_clock()
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
            await self.play_note(note)

        self.__rshift__(self.play(beat, note))

    async def play_target(self, name: str, cur_time: int, target: Time, 
                          note: int):
        """ Play a note in the future at given Time target """
        # print(f"{name}: {cur_time}")
        while self.tick_time < cur_time + target.target():
            await asyncio.sleep(0.0)
        await self.play_note(note)
        # print(f"{name} : {self.get_tick_time()}")
 
        self.__rshift__(self.play_target(
            name=name, cur_time=clock.get_tick_time(),
            target=target, note=note))

# ----------------------------------------------------------------------
# Playground: test code to be imported with library here :)

uvloop.install()
clock = Clock("MIDI Bus 1")
# midi.debug = True

def reset():
    midi.send_stop()
    midi.send_reset()

asyncio.create_task(clock.send_start(initial=True))


cur_time = clock.get_tick_time()
print(f"{cur_time}")

clock >> clock.play_target(name="[bold red] a", cur_time=cur_time, target=Time(24, 1), note=48)
clock >> clock.play_target(name="[bold red] b", cur_time=cur_time, target=Time(24, 1), note=60)
clock >> clock.play_target(name="[bold red] c", cur_time=cur_time, target=Time(24, 1), note=64)
clock >> clock.play_target(name="[bold red] d", cur_time=cur_time, target=Time(24, 1), note=67)
clock >> clock.play_target(name="[bold yellow] 1", cur_time=cur_time, target=Time(24, 0, 3), note=48+24)
clock >> clock.play_target(name="[bold yellow] 2", cur_time=cur_time, target=Time(24, 0, 3), note=60+24)
clock >> clock.play_target(name="[bold yellow] 3", cur_time=cur_time, target=Time(24, 0, 3), note=64+24)
clock >> clock.play_target(name="[bold yellow] 4", cur_time=cur_time, target=Time(24, 0, 3), note=67+24)
