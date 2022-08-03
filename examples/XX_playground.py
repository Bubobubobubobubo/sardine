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
arpeggio = cycle([36, 48, 60])
arpeggio2 = cycle([36, 48, 60])
@die
async def midi_tester(delay=0):
    note(1, next(arpeggio), 127, 1)
    note(1, next(arpeggio2) + 24, 127, 1)
    cs(midi_tester, delay=0.5)

from random import random
import itertools


def bin(sequence: str):
    binary = []
    for char in sequence.replace(' ', ''):
        binary.append(True) if char=="1" else binary.append(False)
    return itertools.cycle(binary)

a = bin('10101010')
b = bin('00000010'*2)
c = bin('10'*4)
arpeg = itertools.cycle([60,72]*2 + [58, 58, 55, 60]*2)
@swim
def two(delay=0.5):
    S('jvbass', midinote=next(arpeg) + 12, amp=1.5).out()
    S('kicklinn', trig= next(a), shape=0.5, amp=1.2).out()
    S('808:9', trig= next(b), shape=0.5, amp=1.2).out()
    S('808:7', trig= next(c), shape=0.5, amp=1.2).out()
    cs(two, delay=0.5)

@die
def one(delay=1):
    S('pluck', midinote=next(arpeggio)).out()
    S('pluck', speed=next(c3) - 2).out()
    cs(one, delay=0.25)


@swim
def three(delay=2):
    S('cp', nb=next(c3)).out()
    cs(three, delay=2)

cr(three)
