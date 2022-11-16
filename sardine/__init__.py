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

from .FishBowl import FishBowl
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
config = read_user_configuration()

#| INITIALISATION |#

# Reading user configuration
config = read_user_configuration()
print_config = pretty_print_configuration_file

bowl = FishBowl(time=Time())
time = bowl.time # passage of time
clock = bowl.clock # clock information
# clock.tempo, clock._beats_per_bar = config.bpm, config.beats

# Adding a parser
bowl.swap_parser(ListParser)

# Adding Senders
bowl.add_handler(MidiHandler())
bowl.add_handler(OSCHandler())
bowl.add_handler(SuperColliderHandler())

# Start clock
bowl.clock.start()