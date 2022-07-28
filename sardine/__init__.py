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

def seq(things):
    return things[c.tick_time % len(things)]

def lfoL(up_to: int):
    l = list(range(up_to))
    return l[c.phase % len(l)]


async def bd(): S("bd").out()
async def hh(): S("hh").out()
async def cp(): S("cp").out()

async def longer():
    S("bd").out()
    await asyncio.sleep(td()*2)
    S("cp").out()
    await asyncio.sleep(td()*4)

async def rand(speed=0, num_iter=0, delay=24):
    if delay > 48:
        delay = 24
    if speed > 10:
        speed = 1
    speed = speed + 1
    num_iter = num_iter + 1
    S('hh', speed=speed).out()
    loop(rand(speed=speed+1, num_iter=num_iter+1, delay=delay*2))

c.ppqn = 96
cs(rand(speed=0, num_iter=0, delay=24))
