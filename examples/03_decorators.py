from sardine import *

from random import choice
from random import randint

# Non-recursive functions can be used as helpers
# They can both be async or synchronous functions
async def random(caller: str = "Nobody"):
    """ Printing a random number"""
    print(f"{caller} : {randint(1,5)}")


# Replace @swim by @die to kill the function
@swim
async def bd(delay=1):
    """ A simple bass drum """
    dur = choice([2, 1])
    await random("bd")
    S('bd', amp=2).out()
    loop(bd(delay=dur))


@swim
async def hh(delay=1):
    """ A simple bass drum """
    dur = choice([2, 1]) / 2
    await random("hh")
    S('hh', amp=2).out()
    loop(hh(delay=dur))

# Regular clock.schedule() and clock.remove() still work!

cr(bd)
cr(hh)

# Exemple minimal

@swim
async def bd():
    print('coucou')
    loop(bd())
