from .clock.Clock import Clock
from .superdirt.Sound import Sound as S
from .superdirt.AutoBoot import SuperColliderProcess, find_startup_file
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from functools import wraps
import uvloop
import asyncio
import pathlib

import warnings
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

SC = SuperColliderProcess(synth_directory=None,
        startup_file=find_startup_file())
SC.boot()

# Pretty printing
print(f"[red]{sardine}[/red]")
print_pre_alpha_todo()
print('\n')

uvloop.install()
c = Clock()
asyncio.create_task(c.send_start(initial=True))
cs, cr, td = c.schedule, c.remove, c._get_tick_duration
loop = c._auto_schedule

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


@swim
async def bd():
    S('bd').out()
    loop(bd())
# 
# @swim
# async def rp(d=0.25):
#     print(f"[1-10] {c.ramp(1, 10)}")
#     print(f"[1-20] {c.ramp(1, 20)}")
#     print(f"[1-40] {c.ramp(20, 40)}")
#     loop(rp(d=0.25))
