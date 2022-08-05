from random import random, randint, choice

from sardine import swim

class Holder:
    pass

@swim
def bd(delay=1):
    S('hh',
            dry=random(),
            room=random(),
            speed=randint(1,4),
            legato=choice([0.1, 0.4]),
            n=randint(1,10)).out()
    cs(bd, delay=choice([1/2,1/4]))


@swim
def hh(delay=1):
    S('bd', n=randint(1,10)).out()
    cs(hh, delay=choice([1, 2/1]))


@swim
def amen(delay=1):
    S('amencutup', n=c.tick).out()
    cs(amen, delay=choice([1, 2/1, 1/2, 1/4, 1/8]))

@swim
def trump(delay=1):
    S('trump',
            n=randint(1,10),
            speed=-0.9,
            legato=0.2,
            trig=d4(1)).out()
    cs(trump, delay=choice([1, 2/1]))

from random import randint
import itertools

a = itertools.cycle([50, 54, 57, 60])
ap = itertools.cycle([50, 54, 57, 60])
b = itertools.cycle([1/2, 1/4, 1, 1/2])
@swim
def test_midi(delay=1/4):
    midinote(random() / 100, n(a), channel=0)
    midinote(random() / 100, n(ap) + 12, channel=0)
    pgch(channel=0, program=randint(1,120))
    cs(test_midi, delay=n(b))
@swim
def test(delay=1):
    S('808',
            n=randint(1,10),
            legato=0.01,
            shape=0.8).out()
    S('bd', trig=1 if random() > 0.8 else 0,
            shape=0.8).out()
    cs(test, delay=1/4)

hush()
