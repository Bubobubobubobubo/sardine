# Writing presets

You can use **Python** dictionaries to write presets for your patterns. It is very simple to do so using the `**` operator that allows you to map dictionaries as keywords. See for yourself:

```python
padcc = { 'timbre': {'control' : 18, 'chan': 2}, 'time': {'control' : 19, 'chan': 2},
        'metal': {'control' : 16, 'chan': 2}, 'fx': {'control' : 17, 'chan': 2}}
basscc = { 'timbre': {'control' : 18, 'chan': 0}, 'time': {'control' : 19, 'chan': 0},
        'cutoff': {'control' : 16, 'chan': 0}, 'fx': {'control' : 17, 'chan': 0}}
jupcc = { 'decay': {'control' : 81, 'chan': 1}, 'time': {'control' : 19, 'chan': 1},
        'cutoff': {'control' : 74, 'chan': 1}, 'resonance': {'control' : 71, 'chan': 1}}

@swim
def structure(p=0.5, i=0):
    N("C2 C3", chan=2, vel=120, i=i)
    N("G5 G4", chan=2, vel=120, i=i, r=0.25/4)
    N("[G6]-[0:12]", chan=2, vel=120, i=i, r=0.25/2)
    CC(**jupcc['cutoff'], value=100) # Here, I am injecting stuff
    CC(**jupcc['decay'], value=80)
    N("[G6]-[0:12]", chan=1, vel=120, i=i, r=0.25/2)
    again(structure, p=0.5, i=i+1)
```

## Effects Presets

Presets are a simple way to pre-load effects with multiple parameters. With multiple versions of an effect (like reverb, delay, etc), you can easily switch between presets with a simple change (**rev1 -> **rev2). Start by "loading" (executing) all of the effects lines.

```python
#effects presets
# reverb
rev0 = {'room':0.9, 'size':0.6, 'dry':0.2}
rev1 = {'room':1.5, 'size':0.8, 'dry':0.8}

#delay
del0 = {'delay':0.5, 'delaytime':0.3, 'delayfeedback':0.3}
del1 = {'delay':0.5, 'delaytime':0.4, 'delayfeedback':0.6}

#distortion
fx0 = {'comb':0.4, 'scram':0.4, 'shape':0.2}
fx1 = {'comb':0.7, 'scram':0.6, 'shape':0.4}

## Effects Presets used in Players
clock.tempo=100
Pb >> d('bd sd ht mt', p='0.5!4 0.25!2', **rev0)

Pb >> d('east:2 east:4 peri:3 east:5', p=0.5, **rev1, **del1)
Pb >> d('east:2 east:4 peri:3 east:5', p=0.25, **rev1, **del0, **fx0)
```
