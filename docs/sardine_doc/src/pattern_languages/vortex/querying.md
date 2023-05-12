# Query pattern values

We have already seen that you can play music using the **TidalCycles** pattern system and **SuperDirt**. **Tidal** can also be used as a value/pattern generator for other things: visuals, sending through OSC, etc. There is a tiny but very welcome mechanism to extract any value from a **Tidal** stream to be reused later in other patterns or for anything else.

Let's start by playing a simple pattern:
```python
d1 * s('kick hat snare hat')
```

Now we can use the `.stream.get('value_name', 0)` method to extract any value name from the pattern being played:
```python
@swim
def gui_loop(p=1/32, i=0):
    # ... doing whatever ...

    blip = d1.stream.get('cycle', 0)
    bloop = d1.stream.get('s', 0)

    my_super_func(blip=blip, bloop=bloop)
    again(gui_loop, p=1/32, i=i+1)
```

Have fun!
