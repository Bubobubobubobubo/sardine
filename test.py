import asyncio

async def nap(duration):
    """ Musical sleep inside coroutines """
    duration = c.tick_time + (duration * c.ppqn)
    while c.tick_time < duration:
        await asyncio.sleep(c._get_tick_duration() / c.ppqn)

async def sync():
    """ Manual resynchronisation """
    cur_bar = c.elapsed_bars
    while c.phase != 1 and c.elapsed_bars != cur_bar + 1:
        await asyncio.sleep(c._get_tick_duration() / c.ppqn)

# cool
@swim
async def bd(delay=1):
    S('bd').out()
    cs(bd, delay=1)

# not cool
@swim
async def hh(delay=1):
    await wait_for_next_bar()
    S('hh').out()
    cs(hh, delay=0.33)



@die
async def cp(delay=0.5):
    S('cp').out()
    await fake_sleep(4)
    S('cp', speed=0.5).out()
    cs(cp, delay=0.5)
