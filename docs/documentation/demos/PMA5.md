# Tribute to Jules Cipher

## Description

Two songs composed by combining **Sardine** with the Roland PMA-5. Everything was recorded with two awful mono jack cables connected to a USB audio soundcard linked through [Carla](https://kx.studio/Applications:Carla) (very high signal-to-noise ratio).

## Performance

<iframe width="1400" height="620" src="https://www.youtube.com/embed/vxypv2C1EII" title="Live-coding in Python - Sounds from Roland PMA-5" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Source code

```python
c.bpm = 125

#LEAD

#marimba
pgch(program=12, channel =0)

#vibraphone
pgch(program=11, channel=0)

@swim
def liquide(d=0.5,i=0):
    #minTheme #disco()                           #div=1
    #M(note = "C@maj", channel = 0).out(i, div = 2)
    #M(note=".!7,<C@min7>,.!7,<C@min7>,.!7,<C@maj7>",
    #        channel = 0).out(i, div=4)
    #LeadTHEME  #apal #^[2~6]
    #M(note="pal(<C@maj, C@min7>,68,65,.,67,.)" , 
    #    velocity = P("70~90",i), 
    #    channel = 0, dur=5000).out(i)
    #Bass lente
    #M(note="disco(<C@maj, C@min7>,68,65,.,67,.)" , 
    #    velocity = P("80~95",i), 
    #    channel = 0, dur=50).out(i, div = 2)
    again(liquide, d=P("0.25, 0.5",i), i=i+1)


#BAss TB303
pgch(program=38, channel=1)
cc(control=0, value =66, channel=1)

Pt >> play_midi(note='C2@min | ., C2@min7', channel = 1)

cc(control=1, value =0, channel=1)

Pt >> None

#DRUMSET 

#TR808
pgch(program=25, channel = 9)

#ROOM2
pgch(program=72, channel = 9)

#TR909
pgch(program=88, channel = 9)

PO >> play_midi(note="36,.,36,.", velocity = 127, channel = 9)

PO >> None

Ps >> play_midi(note=".,.,38,.", velocity = 100, channel = 9)

Ps >> None

Ph >> play_midi(note="44!7,46", channel=9)

Ph >> None
```
