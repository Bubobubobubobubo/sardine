# https://stackoverflow.com/questions/53689193/how-to-handle-exceptions-from-any-task-in-an-event-loop

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
import uvloop
import asyncio
import pathlib

# import warnings
# warnings.filterwarnings("ignore")

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

uvloop.install()

# Are the aliases good?
c = Clock()
cs = c.schedule
cr = c.remove


try:
    asyncio.create_task(c.send_start(initial=True))
except Exception as e:
    print(e)

# Should start, doesn't start
SC = SuperColliderProcess(
        synth_directory=find_synth_directory(),
        startup_file=find_startup_file())

def swim(fn):
    @wraps(fn)
    def decorator(fn):
        try:
            cs(fn())
        except Exception:
            pass
    decorator(fn)
    return fn

def die(fn):
    @wraps(fn)
    def decorator(fn):
        try:
            cr(fn)
        except Exception:
            pass
    return decorator(fn)

from random import random, randint, choice
from itertools import cycle

dur = cycle([0.5, 1, 2])

async def bd(delay=1):
    dura = next(dur)
    S('bd').out()
    cs(bd, delay=dura)

async def bd_stable(delay=1):
    S('bd', shape=0.5).out()
    cs(bd, delay=1)

# async def bd2(delay=1):
#    S('bd', speed=2).out() ; cs(bd2, delay=delay)

cs(bd)
# cs(bd_stable)

# cs(bd2)
