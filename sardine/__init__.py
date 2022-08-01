from .clock.Clock import Clock
from .superdirt.Sound import Sound as S
from .superdirt.AutoBoot import (
        SuperColliderProcess,
        find_startup_file,
        find_synth_directory)
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from functools import wraps
from random import random, randint, choice
from itertools import cycle
import uvloop
import platform
import asyncio
import pathlib
import warnings

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

# UVLoop is not supported on Windows
if platform.system() != "Windows":
    uvloop.install()
warnings.filterwarnings("ignore")

c = Clock()
cs = c.schedule
cr = c.remove


asyncio.create_task(c.send_start(initial=True))

# Should start, doesn't start
SC = SuperColliderProcess(
        synth_directory=find_synth_directory(),
        startup_file=find_startup_file())

def swim(fn):
    """ Push a coroutine on the clock """
    @wraps(fn)
    def decorator(fn):
        try:
            cs(fn())
        except Exception:
            pass
    decorator(fn)
    return fn

def die(fn):
    """ Remove a coroutine from the clock """
    @wraps(fn)
    def decorator(fn):
        try:
            cr(fn)
        except Exception:
            pass
    return decorator(fn)

async def bd(delay=1):
    S('bd').out()
    cs(bd, delay=1)

cs(bd)
