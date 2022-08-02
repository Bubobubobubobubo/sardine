# This file is a playground.
# This is where I test stuff that might break :)

from itertools import cycle
from random import random, randint, choice
from random import random, randint, choice

from sardine import swim
def seq(*args):
    return cycle(list(args))
a = seq(1,2,3)
b = cycle(range(1, 20))
note = cycle([60, 63, 60, 60, 65])
cr(bd)


@swim
async def bd(d=1):
    S('bd' if random() > 0.8 else 'drum').out()
    loop(bd(d=0.5))



@die
async def cut(d=5):
    S('bd', n=3, speed=1).out()
    loop(cut(d=4))


@die
async def bass(d=1):
    # S('jvbass' if random() > 0.5 else ['numbers', 'jvbass'],
    #         room= 0.5 if random() > 0.5 else 0,
    #         speed=choice([1,2,4]),
    #         legato=0.05,
    #         midinote=next(note) - choice([12,24]), amp=1).out()
    loop(bass(d=1))

# Radical changes

@die
async def bd(d=1):
    S('bd' if random() > 0.8 else 'drum').out()
    loop(bd(d=0.5))

@swim
async def printer():
    print('doudou')
    cs(printer())


from itertools import cycle
from random import randint
arpeggio = cycle([60, 64, 67, 71])
@swim
async def midi_tester(delay=0.25):
    note(1, next(arpeggio), 127, 1)
    cc(channel=1, control=20, value=randint(1,127))
    cs(midi_tester, delay=0.25)
