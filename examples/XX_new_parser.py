
from random import choice

@swim
def bd_or_clap(delay=1, iter=0):
    S('bd!3 cp',
            trig=1,
            speed='1!3 0.5',
            room='0 0.3 0.5',
            squiz=2).out(iterator=iter)
    cs(bd_or_clap, delay=1, iter=iter+1)


@swim
def bd_or_clap(delay=1, iter=0):
    S('bd!3 cp',
            trig=1,
            speed='1!3 0.5',
            room='0.0:0.8',
            squiz=2).out(iterator=iter)
    cs(bd_or_clap, delay=1, iter=iter+1)

hush()
