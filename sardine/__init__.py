from __future__ import with_statement
import asyncio
import pathlib
import warnings

from rich import print
from rich.console import Console
from rich.markdown import Markdown
try:
    import uvloop
except ImportError:
    warnings.warn('uvloop is not installed, rhythm accuracy may be impacted')
else:
    uvloop.install()

from .io import read_user_configuration
from .clock import Clock
from .superdirt import (
        SuperColliderProcess,
        find_startup_file,
        find_synth_directory)
from .io import Client as OSC
from typing import Union
from .sequences import *

warnings.filterwarnings("ignore")

def print_pre_alpha_todo() -> None:
    """ Print the TODOlist from pre-alpha version """
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

Sardine is a small MIDI/OSC sequencer made for live-
coding. Check the examples/ folder to learn more. :)
"""


# Pretty printing
print(f"[red]{sardine}[/red]")
print_pre_alpha_todo()
print('\n')


#==============================================================================#
# Initialisation
# - Clock and various aliases
# - SuperDirtProcess (not working)
# - MidiIO basic functions
# - Nap and Sync
#==============================================================================#

config = read_user_configuration()
c = Clock(
        midi_port=config.midi,
        bpm=config.bpm,
        beats_per_bar=config.beats,
        ppqn=config.ppqn)

cs, cr = c.schedule_func, c.remove
children = c.print_children
S = c.note


n = next


def hush():
    """ Stop all runners """
    for runner in c.runners.values():
        runner.stop()


def note(delay, note: int=60, velocity: int=127, channel: int=1):
    """ Send a MIDI Note """
    asyncio.create_task(c._midi.note(
        clock=c, delay=delay, note=note,
            velocity=velocity, channel=channel))


def cc(channel: int=1, control: int=20, value: int=64):
    asyncio.create_task(c._midi.control_change(
        channel=channel, control=control, value=value))


def swim(fn):
    """ Push a function to the clock """
    cs(fn)
    return fn


def die(fn):
    """ Remove a function from the clock """
    cr(fn)
    return fn


c.start()

# Tests
# =====
