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
    S('pluck:9', n=1, trig='1').out(i=i)
    # S('c|a b?', n=9, trig='1 0 1', speed='1:4').out(i=i)
    # S('e|d|h|b|c', n=int(i % 10), trig='1 1 0 0 1 0', speed='3').out(i=i)
    cs(dumb, delay=choice([1/3, 2/3]), i=i+1)

hush()
