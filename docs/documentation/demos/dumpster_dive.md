# dumpsterDive (11/11/2022)

## Description

**dumpsterDive** is a short piece that can be performed with quasi live-coding practices. It uses a set of percussive field recordings made with a 
hard marimba mallet on various parts of a public metal dumpster. One sound was made with a plastic scraper. They are particularly resonant sounds that work well together. The Sardine function uses the stacked samples model, where each sample line can be played alone or together with others. 

- Audio equipment: **Tascam DR-100**, **Rode shotgun mic: NTG4**. 
- Software: **Sardine**
- Dumpster samples are available via the [sardine-sounds](https://github.com/Bubobubobubobubo/sardine-sounds) repository. 

## Performance: composed quasi live-coding

<iframe width="1424" height="600" src="https://www.youtube.com/embed/ZcdXgeqJI2E" title="dumpsterDive" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Source code

```python
# Load audio effect and preset dictionaries first.
# Play one or both lines from each section (basic, reverse rhythms, melodic patterns, bass, scrape). Explore combinations. 

c.bpm=60

@swim
def dumpsterDive(d=1, i=0):
## basic samples - cycle thru the sounds used by all layers 
    S('dumpster:[0,1,4,2,5,3,.!2]', speed=1, amp=.5, **rev1, orbit=0).out(i, div=8) 
    #S('dumpster:[2,0,1,4,3,5]', speed='2', pan=.7, amp=.5, **rev1, orbit=1).out(i, div=2) #**del1
## reverse rhythms
    #S('dumpster:1', begin=.065, end=.4, speed='-1', pan='[.14:.84,0.1],[.83:.15,0.1]', amp=.8, **rev0, orbit=2).out(i, div4)
    #S('dumpster:0!2,.', begin=0, end=.85, speed='1,-1', pan='[.9:.1,0.2],[.1:.9,0.2]', amp=.6, **rev1, orbit=3).out(i, rate=1, div=2) #**del1, 
## melodic patterns
    #S('dumpster:[1!2,4!2,5!2,4]', begin=.052, end=.088, freq='[414,240,620,.,500,380,820,750]', timescale=1.4, pan='[.1,.9]', amp=.95, **rev2, orbit=4).out(i, rate=1, div=1) 
    #S('dumpster:[0,1,0,3,4,]', begin='0', end='.2',speed='1', amp=.6, pan=.3, **rev1, orbit=5).out(i, rate=1, div=2) 
    #S('dumpster:[6!2,8!3,7!2]', octave='7', cut=1, pan=.3, amp=.9, **rev2, orbit=6).out(i, div=4)
## bass - choose one or the other
    #S('dumpster:[2,1,0,.,4,1]', octave=4, amp=.5, **rev1, orbit=7).out(i, rate=1, div=4) 
    #S('dumpster:2', octave='[4.8:5.1,.04],[4.6:4.8,.04]', amp=.95, **rev1, orbit=8).out(i, div=4) 
## scrape
    #S('dumpster:[5,.,5]', octave='6', cut=1, amp=1.2, **del1, **rev1, orbit=8).out(i, rate=.5, div=4) 
    #S('dumpster:[5,.,5]', octave='[6!3,6.62,5.4]', cut=1, amp=.9, **rev2, orbit=9).out(i, rate=1, div=1) #**del2
## presets
    #returnGroove['bass1'].out(i, rate=1, div=4)
    #returnGroove['melody2'].out(i, rate=1, div=2)
    #closing['basic2'].out(i, div=2)
    #closing['basic2a'].out(i, rate=2, div=2) ## div=1
    #closing['scrape2'].out(i, rate=1, div=2)
    #c.bpm = P('[60:90,.03]', i) #accelerate tempo at the end
    
    a(dumpsterDive, d=1/8, i=i+1)

######################################################
#hush(dumpsterDive)

######################## LOAD THESE FIRST - python dictionarys referenced in dumpsterDive function #################
c.bpm=60
## audio effects 
rev0 = {'room':.8, 'size':0.5, 'dry':0.5}
rev1 = {'room':.9, 'size':0.6, 'dry':0.4}
rev2 = {'room':1.5, 'size':0.7, 'dry':0.4}
rev3 = {'room':2, 'size':0.8, 'dry':0.3}

del0 = {'delay':0.5, 'delaytime':0.3, 'delayfeedback':0.5, 'triode':0}
del1 = {'delay':0.5, 'delaytime':0.4, 'delayfeedback':0.6}
del2 = {'delay':0.5, 'delaytime':0.25, 'delayfeedback':0.8}

#Presets
returnGroove = {'bass1':  S('dumpster:[2,1,0,.,4,1]', octave=4, amp=.5, **rev1, orbit=7), 
    'melody2': S('dumpster:[0,1,0,3,4,]', begin='0', end='.2',speed='1', amp=.4, pan=.3, **rev1, orbit=5) }
closing = {'basic2': S('dumpster:[12,0,1,4,3,5]', speed='2', pan=.7, amp=.5, **del1, **rev1, orbit=1), 
    'basic2a': S('dumpster:[0,5,3,4,3,0]', speed='[2.01:1.96,.01],[1.96:2.01,.01]', pan='[.99:.01,0.3],[.01:.99,0.3]', amp=.7, **rev1, **del2, orbit=1), 
    'scrape2': S('dumpster:[5,.,5]', octave='[6!3,6.62,5.4]', cut=1, amp=.9, **del2, **rev2, orbit=9) }
```
Thanks to @Bubobubobubobubo for assistance on Sardine usage. 
