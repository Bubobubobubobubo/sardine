from random import random, randint

from sardine import swim
c.bpm = 120
ct = 0

@swim
def test(delay=0.5, iter=0):
    global ct
    ct += 0.5
    if ct % 2.5 == 0:
        S('bd').out()
        S('jvbass', n=randint(1,20)).out()
    if ct % 3.5 == 0:
        S('cp', n=randint(1,20)).out()
        S('jvbass', n=randint(1,20)).out()
    if ct % 0.5 == 0:
        S('hh', amp=0.4).out()
    cs(test, delay=0.5, iter=iter+1)


hush()

@swim
def new_parser(delay=1, i=0):
    S('amencutup:(1:10)',
            lpf='1->10*100',
            legato=2,
            speed='1').out(i)
    S('world:(1:10)',
            legato='[0.1,0.2]+(0.5)',
            speed='r*(4|-4)').out(i)
    cs(new_parser, delay=0.5, i=i+1)

hush()
