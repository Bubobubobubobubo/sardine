from sardine import *

from random import choice


async def bd(delay=1):
    """ A simple bass drum """
    dur = choice([2, 1])
    S('bd').out()
    loop(bd(delay=dur))

async def hh(delay=0.5):
    """ A simple hihat """
    dur = choice([0.5, 1, 0.5])
    S('hh').out()
    loop(hh(delay=dur))


cs(bd(1))
cs(hh(0.5))

# You can reevalute functions on-the-fly when they
# are scheduled!

async def hh(delay=0.5):
    """ A simple hihat """
    dur = choice([0.5, 1, 0.5])
    S('hh').out()
    loop(hh(delay=dur))

cr(bd)
cr(hh)
