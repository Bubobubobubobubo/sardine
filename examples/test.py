# Wait until the library is imported
# Follow the prompt
from sardine import *

from random import random, choice

# Define asynchronous functions as your score
# You can redefine these on the fly. They will
# be picked up as long as they are ready to be
# scheduled!

# Every function must include a delay argument
# to be valid. This value will be used by the
# system to know when to enter, etc...


async def baba(delay=40):
    duration = 40
    S('bd' if random() > 0.5 else 'cp',
            squiz=2 if random() > 0.5 else 4,
            room=1 if random() > 0.8 else 0.2,
            speed=1 if random() > 0.5 else 0.99).out()
    loop(baba(delay=duration))

async def dada(delay=40):
    S('bd', n=5, speed=1).out()
    loop(dada(delay=80))

async def lala(delay=40):
    S('bd', n=10, speed=2).out()
    loop(lala(delay=80))

# Start a function using cs (clock.schedule)

cs(lala(delay=80))

cr(lala)

c >> lala(delay=80)

c >> bd(delay=20)

c >> dada(delay=80)

c >> lala(delay=80)

# Stop a function using cr (clock.remove)

c << baba
c << dada
c << lala

cr(baba)
cr(dada)
cr(lala)

cr(bd)

# After playing, a list of remaining issues:
# - functions can get desynchronised sometimes.
#   - a cue mechanism could be added!
# - weird crash in console needs a fix.

# I don't really think that the mechanism that is supposed
# to wait before a function starts really works. Might come
# from here.

# I need to work on the duration thing because I can't stay
# with this system forever. I need to use the clock to do
# something that is really stable and that will work.

# Inject a default delay duration inside the coroutine that
# is about to start in clock.schedule.

# I am not catching tasks. I only catch coroutines. I need
# to do something about this.
