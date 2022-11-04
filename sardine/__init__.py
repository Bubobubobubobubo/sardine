# SARDINE: this is the main entry point for Sardine. __init__.py will attempt
# to load everything needed for an interactive session directly from here.
# Linters might complain about the fact some objects are not accessed. Sure,
# they are not accessed right now but will later in time when the user will
# start interacting with the system.

from random import random, randint, choice
from math import floor
from rich import print
import asyncio
import warnings
import sys

try:
    import uvloop
except ImportError:
    print("[yellow]UVLoop is not installed. Not supported on Windows![/yellow]")
    print("[yellow]Rhythm accuracy may be impacted[/yellow]")
else:
    uvloop.install()

from random import random, randint, choice
from typing import Union, Any
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich import pretty
from .io import read_user_configuration, pretty_print_configuration_file
from .io import ClockListener, MidiListener, ControlTarget, NoteTarget
from .clock import *
from .superdirt import SuperColliderProcess
from .io import Client as OSC
from .io import Receiver as Receiver
from .io import OSCSender, MIDISender

from .sequences import ListParser
from .sequences.Iterators import Iterator
from .sequences.Variables import Variables
from .sequences.Sequence import E, euclid, mod, imod, pick, text_eater
from .sequences.LexerParser.FuncLibrary import qualifiers
from .sequences import *

warnings.filterwarnings("ignore")
# Use rich print by default
pretty.install()


def _ticked(condition: bool):
    """Print an ASCII Art [X] if True or [ ] if false"""
    return "[X]" if condition else "[ ]"


# Reading / Creating / Updating the configuration file
config = read_user_configuration()
print_config = pretty_print_configuration_file

sardine = """
░██████╗░█████╗░██████╗░██████╗░██╗███╗░░██╗███████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║████╗░██║██╔════╝
╚█████╗░███████║██████╔╝██║░░██║██║██╔██╗██║█████╗░░
░╚═══██╗██╔══██║██╔══██╗██║░░██║██║██║╚████║██╔══╝░░
██████╔╝██║░░██║██║░░██║██████╔╝██║██║░╚███║███████╗
╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝╚══════╝

Sardine is a MIDI/OSC sequencer made for live-coding
Play music, read the docs, contribute, and have fun!
WEBSITE: [yellow]https://sardine.raphaelforment.fr[/yellow]
GITHUB: [yellow]https://github.com/Bubobubobubobubo/sardine[/yellow]
"""
from rich.panel import Panel

print(Panel.fit(f"[red]{sardine}[/red]"))

print(
    f" [yellow]BPM: [red]{config.bpm}[/red],",
    f"[yellow]BEATS: [red]{config.beats}[/red]",
    f"[yellow]SC: [red]{_ticked(config.boot_superdirt)}[/red],",
    f"[yellow]DEFER: [red]{_ticked(config.deferred_scheduling)}[/red]",
    f"[yellow]MIDI: [red]{config.midi}[/red]",
)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# Here starts the complex and convoluted session setup process. #
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

# Booting SuperCollider / SuperDirt
if config.boot_superdirt is True:
    try:
        SC = SuperColliderProcess(
            startup_file=config.superdirt_config_path,  # config file
            verbose=config.verbose_superdirt,  # verbosity for SC output
        )
    except OSError as error:
        print("[red]SuperCollider could not be found![/red]")
else:
    print("[green]Booting without SuperCollider![/green]")

# Starting the default Clock
c = Clock(
    midi_port=config.midi,  # default MIDI port
    bpm=config.bpm,  # default BPM configuration
    beats_per_bar=config.beats,  # default beats per bar
    ppqn=config.ppqn,  # default pulses per quarter note (MIDI/Clock related)
    deferred_scheduling=config.deferred_scheduling,  # Clock related
)

# Synonyms for swimming function management
cs = again = anew = a = c.schedule_func  # aliases for recursion
cr = stop = c.remove
children = c.print_children

# Senders: the most important I/O objects
S = c.note  # default SuperDirt Sender
M = c.midinote  # default Midi Sender
O = c.oscmessage  # default OSC Sender

MidiSend = MIDISender


def hush(*args):
    """
    Name taken from Tidal. This is the most basic function to stop function(s)
    from being called again. Will silence all functions by default. You can
    also specify one or more functions to be stopped, keeping the others alive.
    """
    if len(args) >= 1:
        for runner in args:
            c.remove(runner)
    else:
        for runner in c.runners.values():
            runner.stop()


def midinote(delay, note: int = 60, velocity: int = 127, channel: int = 1):
    """Helper function to send a MIDI Note"""
    asyncio.create_task(
        c._midi.note(delay=delay, note=note, velocity=velocity, channel=channel)
    )


def cc(channel: int = 0, control: int = 20, value: int = 64):
    """Control Changes (MIDI). Send a Control Change"""
    asyncio.create_task(
        c._midi.control_change(channel=channel, control=control, value=value)
    )


def pgch(channel: int = 0, program: int = 0):
    """Program Changes (MIDI). Send a Program Change"""
    asyncio.create_task(c._midi.program_change(channel=channel, program=program))


def pwheel(channel: int = 0, pitch: int = 0):
    """Pitchwheel (MIDI). Send a pitchweel message. For people looking at
    the modwheel, this is usually done through control changes."""
    asyncio.create_task(c._midi.pitchwheel(channel=channel, pitch=pitch))


def sysex(data: list[int]):
    """
    Sysex Messages (MIDI). Non-standard MIDI messages, usually used by
    some manufacturers to send custom messages and to provide more detailed
    controls. Frequently used on older synths.
    """
    asyncio.create_task(c._midi.sysex(data))


def swim(fn):
    """
    Swimming decorator: push a function to the clock. The function will be
    declared and followed by the clock system to recurse in time if needed.
    """
    cs(fn)
    return fn


def die(fn):
    """
    Swimming decorator: remove a function from the clock. The function will not
    be called again and will likely stop recursing in time.
    """
    cr(fn)
    return fn


drown = die


def sleep(n_beats: Union[int, float]):
    """Artificially sleep in the current function for `n_beats`.

    Example usage: ::

        @swim
        def func(delay=4):
            sleep(3)
            for _ in range(3):
                S('909').out()
                sleep(1/2)
            cs(func)

    This should *only* be called inside functions scheduled by the clock.
    Calling this outside of a scheduled function will result in
    abnormal behavior such as overlapping sounds and clock desync.

    Using in asynchronous functions
    -------------------------------

    This can be used in `async def` functions and does *not* need to be awaited.

    Sounds scheduled in asynchronous functions will be influenced by
    real time passing. For example, if you sleep for 48 ticks and
    await a function that takes 5 ticks to complete, any sounds sent
    afterwards will occur 53 ticks from when the function was called (48 + 5).

    ::

        @swim
        async def func(delay=4):
            print(c.tick)  # 0

            sleep(1)       # +48 virtual ticks (assuming c.ppqn = 48)
            await abc()    # +5 real-time ticks

            S('bd').out()  # occurs 48 ticks from now
            print(c.tick)  # 53
            cs(func)

    Technical Details
    -----------------

    Unlike `time.sleep(n)`, this function does not actually block
    the function from running. Instead, it temporarily affects the
    value of `Clock.tick` and extends the perceived time of other
    Clock methods like `Clock.wait_after()` and `Clock.get_beat_ticks()`.

    In essence, this maintains the precision of sound scheduling
    without requiring the use of declarative syntax like
    `S('909', at=1/2).out()`.

    """
    ticks = c.get_beat_ticks(n_beats, sync=False)
    c.tick_shift += ticks


# IMPORTANT: this is where the clock starts being active (looping infinitely).
c.start(active=config.active_clock)


# Loading user_configuration.py from configuration folder
import importlib

if Path(f"{config.user_config_path}").is_file():
    spec = importlib.util.spec_from_file_location(
        "user_configuration", config.user_config_path
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    from user_configuration import *
else:
    print(f"[red]No user provided configuration file found...")


# Debugging parser: pure Sardine pattern syntax parser. Used for debugging when
# developping Sardine. Will print the AST and result of a given operation.


def parser(pattern: str):
    """Parse a single expression and get result"""
    parser = ListParser()
    print(parser.parse(pattern))


def parser_repl(parser_type: str) -> None:
    """Parse a single expression and get result"""
    parser = ListParser(
        clock=c, iterators=c.iterators, variables=c.variables, parser_type=parser_type
    )

    def _exit_case(string):
        if string.lower() == "exit":
            return True

    try:
        while True:
            user_input = input("> ")
            if _exit_case(user_input):
                break
            else:
                p = parser._parse_debug(pattern=user_input)
    except KeyboardInterrupt:
        pass


def lang_debug() -> None:
    """Debug mode for language dev"""
    return parser_repl(parser_type="proto")


# Interface to the patterning system
def Pat(pattern: str, i: int = 0, div: int = 1, rate: int = 1) -> Any:
    """Generates a pattern

    Args:
        pattern (str): A pattern to be parsed
        i (int, optional): Index for iterators. Defaults to 0.

    Returns:
        int: The ith element from the resulting pattern
    """
    parser = c.parser
    result = parser.parse(pattern)

    def _pattern_element(div: int, rate: int, iterator: int, pattern: list) -> Any:
        """Joseph Enguehard's algorithm for solving iteration speed"""
        return floor(iterator * rate / div) % len(pattern)

    return result[_pattern_element(div=div, rate=rate, iterator=i, pattern=result)]


def print_scales() -> None:
    """Print the list of built-in scales and chords"""
    """Print all available scales in the patterning system"""
    print(qualifiers.keys())


def panic() -> None:
    """Panic function, will cut everything"""
    hush()  # Stop everything
    S("superpanic").out()  # Superpanic is a synth capable of
    # cutting every other synth


def print_qualities():
    """Return the list of qualifiers"""
    return qualifiers


class Delay:
    """
    with delay(0.5):
        do_stuff()
    """

    def __init__(self, duration: Union[int, float] = 1, delayFirst: bool = True):
        """
        This compound statements needs to know two things, already provided
        by some default values:
        duration: for how long do we wait before or after the block?
        delayFirst: are we waiting before or after the block?
        """
        self.duration = duration
        self.delayFirst = delayFirst

    def __call__(self, duration=1, delayFirst=False):
        self.duration = duration
        self.delayFirst = delayFirst
        return self

    def __enter__(self):
        if self.delayFirst:
            sleep(self.duration)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.delayFirst:
            sleep(self.duration)


# Amphibian iterators and amphibian variables
i, v = c.iterators, c.variables
P = Pat

if config.debug:
    try:
        lang_debug()
    except Exception as e:
        lang_debug()
