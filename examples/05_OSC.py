from random import randint, random, chance

# Open a new OSC connexion
my_osc = OSC(ip="127.0.0.1",
        port= 23000, name="Bibu",
        ahead_amount=0.25)

# Recursive function sending OSC
@swim
async def custom_osc(delay=1):
    my_osc.send('/coucou', [randint(1,10), randint(1,100)])
    cs(custom_osc, delay=1)

# Closing and getting rid of the connexion

cr(custom_osc)

del my_osc
