from __future__ import with_statement
import asyncio
import pathlib
import warnings
import sys

from rich import print
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown

try:
    import uvloop
except ImportError:
    warnings.warn("uvloop is not installed, rhythm accuracy may be impacted")
else:
    uvloop.install()

from .io import read_user_configuration
from .io import ClockListener, MidiListener, ControlTarget, NoteTarget
from .clock import *
from .superdirt import SuperColliderProcess
from .io import Client as OSC
from .io import (
        OSCSender,
        MIDISender)
from .sequences import ListParser
from typing import Union
from .sequences import *

warnings.filterwarnings("ignore")


def print_pre_alpha_todo() -> None:
    """Print the TODOlist from pre-alpha version"""
    cur_path = pathlib.Path(__file__).parent.resolve()
    with open("".join([str(cur_path), "/todo.md"])) as f:
        console = Console()
        console.print(Markdown(f.read()))


sardine = """

░██████╗░█████╗░██████╗░██████╗░██╗███╗░░██╗███████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║████╗░██║██╔════╝
╚█████╗░███████║██████╔╝██║░░██║██║██╔██╗██║█████╗░░
░╚═══██╗██╔══██║██╔══██╗██║░░██║██║██║╚████║██╔══╝░░
██████╔╝██║░░██║██║░░██║██████╔╝██║██║░╚███║███████╗
╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝╚══════╝

Sardine is a MIDI/OSC sequencer made for live-coding.
Play music, read the docs, contribute, and have fun!
"""
print(f"[red]{sardine}[/red]")
config = read_user_configuration()


if config.boot_superdirt:
    SC = SuperColliderProcess(startup_file=config.superdirt_config_path)


c = Clock(
    midi_port=config.midi,
    bpm=config.bpm,
    beats_per_bar=config.beats,
    ppqn=config.ppqn,
    deferred_scheduling=config.deferred_scheduling,
)
cs, again, cr = c.schedule_func, c.schedule_func, c.remove
children = c.print_children
S = c.note
O = OSCSender
M = MIDISender
n = next


def hush():
    """Stop all runners"""
    for runner in c.runners.values():
        runner.stop()


def midinote(delay, note: int = 60, velocity: int = 127, channel: int = 1):
    """Send a MIDI Note"""
    asyncio.create_task(
        c._midi.note(delay=delay, note=note, velocity=velocity, channel=channel)
    )


def cc(channel: int = 1, control: int = 20, value: int = 64):
    asyncio.create_task(
        c._midi.control_change(channel=channel, control=control, value=value)
    )


def pgch(channel: int = 1, program: int = 0):
    asyncio.create_task(c._midi.program_change(channel=channel, program=program))


def pwheel(channel: int = 1, pitch: int = 0):
    asyncio.create_task(c._midi.pitchwheel(channel=channel, pitch=pitch))


def swim(fn):
    """Push a function to the clock"""
    cs(fn)
    return fn


def die(fn):
    """Remove a function from the clock"""
    cr(fn)
    return fn


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
    c.shift_ctx(ticks)


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

def parser(pattern: str):
    """Parse a single expression and get result"""
    parser = ListParser()
    print(parser.parse(pattern))

def parser_repl():
    """Parse a single expression and get result"""
    parser = ListParser()
    try:
        while True:
            p = parser._parse_debug(pattern=input('> '))
            print(p)
    except KeyboardInterrupt:
        pass