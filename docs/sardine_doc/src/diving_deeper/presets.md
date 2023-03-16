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
