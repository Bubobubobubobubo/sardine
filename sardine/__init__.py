from .Clock import Clock
from .Sound import Sound as S
from rich import print
from typing import Union
from functools import wraps
import uvloop
import asyncio

# Dirty hack
import warnings
warnings.filterwarnings("ignore")

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

print(f"[blink]{sardine}[/blink]")
uvloop.install()
c = Clock()
asyncio.create_task(c.send_start(initial=True))
cs, cr, td = c.schedule, c.remove, c._get_tick_duration
loop = c._auto_schedule

def swim(fn):
    @wraps(fn)
    def decorator(fn):
        cs(fn())
    decorator(fn)
    return fn

def die(fn):
    @wraps(fn)
    def decorator(fn):
        cr(fn)
    return decorator(fn)

# @swim
# async def bd(delay=1):
#     S('bd').out()
#     loop(bd(delay=1))
