from .Clock import Clock
from .Sound import Sound as S
from rich import print
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
