from random import choice

M(c, c._midi, delay=0.3, note='50-12|24 57 59 50+0|12|24', velocity='60+r*60', channel=0).out()

M(delay= 0.1, '60|67|52|59', 127, 0).out()

hush()

from random import choice
@swim
def note_midi(d=1, i=0):
    M(delay=0.3,
            trig='1 1|0 1 1',
            note='50-12|24 57 59 50+0|12|24',
            velocity='60+r*60',
            channel=0).out(i)
    M(delay=0.3,
            trig='1 1|0 1 1',
            note='50-12|24+12 57+12 59+12 50+0|12|24',
            velocity='60+r*60',
            channel=0).out(i)
    anew(note_midi, d=choice([1/3, 2/3]), i=i+1)

@swim
def bd(d=2, i=0):
    S('k', speed='0.25|0.5|1', amp=1).out(i)
    if often():
        S('a|b|c|k:r*9', amp=0.2, room=0.5, dry=0.2, legato=0.1, speed='r/2').out(i)
    if rarely():
        S('a|b|c|k:r*9', amp=0.2, speed='1').out(i)
    anew(bd, d=choice([1/3*4, 1/3*2, 1/3]), i=i+1)

@swim
def note_midi2(d=1, i=0):
    M(c, c._midi, delay=0.3,
            trig='1 1|0 1 1',
            note='62 65 69 72',
            velocity='60+r*60',
            channel=0).out(i)
    if rarely():
        M(c, c._midi, delay=0.8, note='62+(24|12|0|-12)',
            velocity='60+r*60', channel=0).out(i)
    anew(note_midi2, d=choice([1/3, 2/3]), i=i+1)

hush()
