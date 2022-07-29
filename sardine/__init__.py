from .Clock import Clock
from .Sound import Sound as S
from rich import print
import uvloop
from math import floor
import asyncio
import random
import itertools

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

async def bd(delay=24):
    S('bd').out()
    loop(bd(delay=delay))

async def incr(delay=24, num=0):
    num += 1
    print(f"Num: {num}")
    loop(incr(delay=delay, num=num))

c.ppqn = 96
# cs(incr(delay=24, num=0))
# cs(bd(delay=24))
