# Clock

There is no difference between the **Sardine** Clock and the **Tidal** Clock. There are a few functions you can use if you are more familiar with the Tidal model:
- `clock.cps`: set the number of cycles per second for your patterns.
  - `(135/60/4)` to set the tempo at 135 beats per minute.
- `clock.get_cps()`: get the `cps` from the current `clock.tempo`.

The `cps` attribute is both a setter and a getter, meaning that you can write:
```python
clock.cps = 0.5 # set the value
clock.cps       # get the value
```

There is no difference between running a pattern using the Internal Clock or using the Link Clock.
