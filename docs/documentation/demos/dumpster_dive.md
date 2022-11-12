# Dumpster Dive (11/11/2022)

## Description

A short piece composed with field recordingd  made with a hard marimba mallet on various parts of a public metal dumpster. One sound was made with a plastic windshield scraper. They are particularly resonant percussive sounds that work well together. 

- Audio equipment: **Tascam DR-100**, **Rode shotgun mic: NTG4**. 
- Software: **Sardine**. 

## Performance

<iframe width="1424" height="600" src="https://www.youtube.com/embed/ZcdXgeqJI2E" title="dumpsterDive" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Source code

```python
# Play one or both lines from each section. Explore combinations. 
c.bpm=60
@swim
def dumpsterDive(d=1, i=0):
## basic samples - cycle thru the sounds used by all layers 
    S('dumpster:[14,15,18,16,19,17,.!2]', speed=1, amp=.5, **rev1, orbit=0).out(i, div=8) 
    #S('dumpster:[16,14,15,18,17,19]', speed='2', pan=.7, amp=.5, **rev1, orbit=1).out(i, div=4) #**del1
## reverse rhythms
    #S('dumpster:15', begin=.065, end=.4, speed='-1', pan='[.14:.84,0.1],[.83:.15,0.1]', amp=.8, **rev0, orbit=2).out(i, div=2)
    #S('dumpster:14!2,.', begin=0, end=.85, speed='1,-1', pan='[.9:.1,0.2],[.1:.9,0.2]', amp=.6, **rev1, orbit=3).out(i, rate=1, div=2) #**del1, 
## melodic patterns
    #S('dumpster:[15!2,18!2,19!2,18]', begin=.052, end=.088, freq='[414,240,620,.,500,380,820,750]', timescale=1.4, pan='[.1,.9]', amp=.95, **rev2, orbit=4).out(i, rate=1, div=1) 
    #S('dumpster:[14,15,14,17,18,]', begin='0', end='.2',speed='1', amp=.6, pan=.3, **rev1, orbit=5).out(i, rate=1, div=2) 
    #S('dumpster:(r*5+10)', octave=7, cut=1, pan=.3, amp=.9, **rev2, orbit=6).out(i, div=4)
## bass - choose one or the other
    #S('dumpster:[16,15,14,.,18,15]', octave=4, amp=.5, **rev1, orbit=7).out(i, rate=1, div=4) 
    #S('dumpster:16', octave='[4.8:5.1,.04],[4.6:4.8,.04]', amp=.95, **rev1, orbit=8).out(i, div=4) 
## scrape
    #S('dumpster:[19,.,19]', octave='6', cut=1, amp=1.2, **del1, **rev1, orbit=8).out(i, rate=.5, div=4) 
    #S('dumpster:[19,.,19]', octave='[6!3,6.62,5.4]', cut=1, amp=.9, **rev2, orbit=9).out(i, rate=1, div=1) #**del2

#hush(dumpsterDive)
```