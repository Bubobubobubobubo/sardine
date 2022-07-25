import asyncio
import itertools
import mido
import time
from rich import print
from typing import Union

class Task:

    """
    Specialised version of an asyncio task meant to be scheduled
    in a temporal context. 
    """

    def __init__(self, callback):
        pass


class MidiIO:

    """
    Naive MIDI Clock implementation.

    Keyword arguments:
    port_name: str -- Exact String for the MIDIOut Port.
    bpm: Union[int, float] -- Clock Tempo in beats per minute
    beats_per_bar: int -- Number of beats in a given bar
    """

    def __init__(self, port_name: str,
                 bpm: Union[float, int] = 120,
                 beat_per_bar: int = 4):

        self._midi_ports = mido.get_output_names()
        if port_name:
            try:
                self._midi = mido.open_output()
            except Exception as error:
                print(f"[bold red]Init error: {error}[/bold red]")
        else:
            try:
                self._midi = mido.open_output(self._midi_ports[0])
            except Exception as error:
                print(f"[bold red]Init error: {error}[/bold red]")
        # Clock maintenance related
        self._background_tasks = set()
        self.running = True
        self._debug = False
        # Timing related
        self._bpm = bpm
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

        # Initialise clock and signal out when ready
        self.send_start()

    # ---------------------------------------------------------------------- #
    # Setters and getters

    def get_bpm(self):
        """ BPM Getter """
        return self._bpm

    def set_bpm(self, new_bpm: Union[int, float]) -> None:
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
        return (60 / self.bpm) / self.ppqn

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
    # Public methods

    def __rshift__(self, function_to_call):
        """ Can I override this? """
        asyncio.create_task(function_to_call)

    async def play_note(self, note: int = 60,
                        channel: int = 0,
                        velocity: int = 127,
                        duration: Union[float, int] = 1) -> None:
        """
        Play note test function
        
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

    def send_start(self) -> None:
        """ MIDI Start message """
        self._midi.send(mido.Message('start'))

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

    def log_clock(self) -> None:
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
        Naive MIDI clock implementation. Drift will happen and will not be
        corrected.

        Keyword arguments:
        debug: bool -- print debug messages on stdout.
        """

        print(f"[bold red]Start clock with port {self._midi_ports[0]}")
        while self.running:
            begin = time.perf_counter()
            await asyncio.sleep(self.tick_duration)
            self.send_clock()
            self.beat += 1
            self._update_phase()
            if self.phase == 1:
                self._update_current_beat()
            if self.beat % self.ppqn == 0:
                self.elapsed_bars += 1
            end = time.perf_counter()
            self.delta = end - begin
            if self._debug:
                self.log_clock()

    async def mod_on(self, modulo: int, note: int):
        """
        Play a note for a specific modulo based on MIDI tick rate.
        modulo: int -- targetted modulo for a note_on playback.
        note: int -- MIDI note to be played.
        """
        while True:
            await asyncio.sleep(0.0)
            if self.phase == modulo:
                await self.play_note(note)

    async def old_beat_on(self, beat: int, note: int):
        """
        Play a note on a specific beat of the current measure.
        beat: int -- targetted beat in the bar.
        note: int -- MIDI note to be played.
        """
        while True:
            await asyncio.sleep(0.0)
            if self.current_beat == beat:
                await self.play_note(note)

    async def beat_on(self, beat: int, note: int):
        """
        Play a note on a specific beat of the current measure.
        beat: int -- targetted beat in the bar.
        note: int -- MIDI note to be played.
        """
        # await asyncio.sleep(0.0)
        if self.current_beat == beat:
            await self.play_note(note)

async def background_services(midi: MidiIO):
    """
    Run some background services (such as the Clock) right when the library
    is imported. This is the equivalent of the main() loop for our asyncio
    event loop.

    midi: MidiIO -- the MIDI output and Clock to be used.
    """
    clock_task = midi.run_clock()
    midi._background_tasks.add(clock_task)

    # To prevent the garbage collector from collecting our tasks
    for task in midi._background_tasks:
        await asyncio.create_task(task)

# ----------------------------------------------------------------------
# Playground: test code to be imported with library here :)

midi = MidiIO("MIDI Bus 1")
sched = asyncio.create_task
sched(background_services(midi))


def reset():
    midi.send_stop()
    midi.send_reset()

# midi >> midi.old_beat_on(1, 60)
# midi >> midi.old_beat_on(2, 64)
# midi >> midi.old_beat_on(3, 67)
# midi >> midi.old_beat_on(4, 72)
