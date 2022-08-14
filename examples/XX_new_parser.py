from random import choice
from random import randint


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
