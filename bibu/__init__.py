from .Clock import Clock
from .Sound import Sound
import itertools
import uvloop
import asyncio

uvloop.install()
clock = Clock("MIDI Bus 1")
clock.debug = False
asyncio.create_task(clock.send_start(initial=True))
T = clock.get_tick_time()

async def bd(): Sound("bd").out()
async def hh(): Sound("hh").out()

clock.schedule(bd, 24)
#clock.schedule(hh, 12)
