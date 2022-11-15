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
from .clock.LinkClock import LinkClock
from .sequences.LexerParser.ListParser import ListParser
from .Handlers import (
    SuperColliderHandler, 
    MidiHandler, OSCHandler)
from .sequences.Iterators import Iterator
from .sequences.Variables import Variables

from .io.UserConfig import (
    read_user_configuration,
    pretty_print_configuration_file)

#| INITIALISATION |#

# Reading user configuration
config = read_user_configuration()
print_config = pretty_print_configuration_file

env = FishBowl(time=Time())
time = env._time # passage of time
clock = env._clock # clock information

# Adding a parser
env.add_parser(ListParser)

# Adding Senders
env.add_handler(MidiHandler())
env.add_handler(OSCHandler())
env.add_handler(SuperColliderHandler())

# Start clock
env.clock.start()