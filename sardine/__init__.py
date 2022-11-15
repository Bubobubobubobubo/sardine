from rich import print

import asyncio
try:
    import uvloop
except ImportError:
    print("[yellow]UVLoop is not installed. Not supported on Windows![/yellow]")
    print("[yellow]Rhythm accuracy may be impacted[/yellow]")
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvloop.install()

from .clock.FishBowl import FishBowl
from .clock.Time import Time
from .clock.InternalClock import Clock
from .sequences.LexerParser.ListParser import ListParser
from .Handlers import (
    SuperColliderHandler, 
    MidiHandler, OSCHandler)
from .sequences.Iterators import Iterator
from .sequences.Variables import Variables


#| INITIALISATION |#

# Environment
env = FishBowl(
    time=Time(
        phase=0,
        beat=0,
        bar=0
    ), 
    clock=Clock())

# Adding a parser
env.add_parser(ListParser)

# Adding Senders
env.add_handler(MidiHandler())
env.add_handler(OSCHandler())
env.add_handler(SuperColliderHandler())