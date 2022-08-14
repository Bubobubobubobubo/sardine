from random import choice
from random import randint

from sardine import swim


# Open a new OSC connexion
my_osc = OSC(ip="127.0.0.1",
        port= 23000, name="Bibu",
        ahead_amount=0.25)

@swim
def bd_or_clap(delay=1, iter=0):
    S('pluck',
            midinote='50!3 54 50!3 50:62',
            speed='1 2 1 4 8?').out(i=iter)
    O(c, my_osc, '/coucou /lala',
            value='1 2 3 4 5').out(i=iter)
    cs(bd_or_clap, delay=0.5, iter=iter+1)

hush()

from random import choice

@swim
def dumb(delay=0.25, i=0):
    S('808bd:2', n=1, trig=euclid(2,8)).out(i=i)
    S('e:2|e:5|e:8', n=1, trig=euclid(1,8)).out(i=i)
    S('h|hh', n=1, legato='0.01:0.1', speed='4:8',
            trig=euclid(4,8)).out(i=i)
    cs(dumb, delay=choice([0.25]), i=i+1)

hush()
