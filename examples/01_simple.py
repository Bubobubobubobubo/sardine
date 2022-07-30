from sardine import *

c.bpm = 100 # change bpm

async def bd(delay=1):
    """ A simple bass drum """
    S('bd').out()
    loop(bd(delay=1))

async def hh(delay=0.5):
    """ A simple hihat """
    S('hh').out()
    loop(hh(delay=0.5))

cs(bd(1)) # triggering everything
cs(hh(0.5)) # triggering everything

cr(bd) # stop the loops
cr(hh)
