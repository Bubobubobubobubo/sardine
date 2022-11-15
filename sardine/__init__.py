from .clock.FishBowl import FishBowl
from .clock.Time import Time
from .clock.InternalClock import Clock
from .sequences.LexerParser import ListParser

#| INITIALISATION |#

# Environment
env = FishBowl(
    time=Time(), 
    clock=Clock(), 
    parser=ListParser())

# Adding Senders
env.add_handler(MidiHandler)
env.add_handler(OSCHandler)
env.add_handler(SuperColliderHandler)