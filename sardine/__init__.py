# https://stackoverflow.com/questions/53689193/how-to-handle-exceptions-from-any-task-in-an-event-loop

import asyncio
from functools import wraps
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

from .clock.Clock import Clock
from .superdirt.Sound import Sound as S
from .superdirt.AutoBoot import (
        SuperColliderProcess,
        find_startup_file,
        find_synth_directory)

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

c = Clock()
cs = c.schedule
cr = c.remove


asyncio.create_task(c.send_start(initial=True))

# Should start, doesn't start
SC = SuperColliderProcess(
        synth_directory=find_synth_directory(),
        startup_file=find_startup_file())

def swim(fn):
    """ Push a function to the clock """
    cs(fn)
    return fn

def die(fn):
    """ Remove a function from the clock """
            cr(fn)
    return fn

async def bd(delay=1):
    S('bd').out()
    cs(bd, delay=1)

cs(bd)
