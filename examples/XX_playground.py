# This file is a playground.
# This is where I test stuff that might break :)


from random import randint

@swim
def bd(delay=1/4):
    c.log() # to fix
    S('jvbass',
            delay=0.5,
            delayfeedback=0.5,
            delaytime=1/2,
            n=randint(1,20)).out()
    note(1, 60, 127, 1)
    S('bd', trig=1 if random() > 0.8 else 0).out()
    cs(bd, delay=1/4)

hush()
