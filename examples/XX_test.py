from random import random, randint, choice
from sardine import swim

cosc  = OSC(ip="127.0.0.1",
        port= 23000, name="Bibu",
        ahead_amount=0.25)
cosc.kill()

from random import random
@swim
def bd(delay=1):
    S('bd').out()
    cosc.send(c, "/coucou", [random()])
    cs(bd, delay=1)


