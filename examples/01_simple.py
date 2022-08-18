from sardine import *

c.bpm = 100  # change bpm


async def bd(delay=1):
    """A simple bass drum"""
    S("bd").out()
    cs(bd, delay=1)


async def hh(delay=0.5):
    """A simple hihat"""
    S("hh").out()
    cs(delay=0.5)


# Push functions on the loop
cs(bd, delay=1)
cs(hh, delay=1)

# Remove functions from the loop
cr(bd)
cr(hh)
