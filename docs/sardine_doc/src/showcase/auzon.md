# D'Auzon

<iframe width="700" height="500" src="https://www.youtube.com/embed/We_qONc9Wbc" title="D&#39;Auzon" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

```python
Live-coding réalisé sous Sardine (sardine.raphaelforment.fr). 
Matière sonore synthétisée et manipulée au travers du live-coding dans Supercollider.

- Rémi

clock.tempo = 60

D("long:5", attack = 1,release =15, accelerate = (-1),gain = 0.5, room = 0.5)
D("long:5", attack = 1,release =15,speed = 0.5, accelerate = (-1),gain = 0.5, room = 0.5)
D("long:5", attack = 1,release =15,speed = 0.6, accelerate = (-1),gain = 0.5, room = 0.5)
D("long:5", attack = 1, release =15,speed = 0.8, accelerate = (-1),gain = 0.5, room = 0.5, sz = 0.6)

@swim
def downsweep(p=0.5, i=1):
    D("long:5", attack = 2, release =10,
            coarse = 6, pan = "rand",
            speed = 0.8, accelerate = "1,-1,2,-2",
            gain = "0.9,0.8,0.9,0.8", room = 0.5, sz = 0.6, i=i)
    again(downsweep,p=P("8,4,16",i), i=i+1)

@swim
def downsweep2(p=0.5, i=1):
    D("long:10", release =2.5,
           # coarse = 6, pan = "rand",
            speed = 0.8,
            #speed = "0.8,0.70,0.75,0.70",scram = "0!8,0.5!2",
            #speed = "0.73,0.75,0.70,0.75,0.75,0.85", scram = "0!2, 0.5!6",
            gain = "1.2,1.1,1.1,1.2", room = 0.2, sz = 0.6, 
            i=i)
    again(downsweep2,p=P("1!2,0.25!4,1!2,0.5!2,16",i), i=i+1)

@swim
def romble(p=0.5,i=1):
    D("long:[1~32]", lpf=100, legato = 2, i=i)
    again(romble,p=P("0.5!32,32",i),i=i+1)

@swim
def shark(p=0.5,i=1):
    D("pluck", scram = 0.2, binshift = 1,
            gain =0.6, i=i)
    D("long:9", legato = 4, 
            i=i)
    again(shark,p=P("4,2,4",i),i=i+1)


panic()


panic()
```
