from .Clock import Clock
from .Sound import Sound as S
from rich import print
from typing import Union
from functools import wraps
import uvloop
import asyncio

# Dirty hack
import warnings
# warnings.filterwarnings("ignore")

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
