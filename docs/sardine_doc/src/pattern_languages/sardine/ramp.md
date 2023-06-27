# Ramp

This operator is analogous to Python's **range()** function, only better.
- Generate a ramp using the `[1:10]` syntax: `[1 2 3 4 5 6 7 8 9 10]`.
- Ramps can go up and down, and even go both directions `(pal [1:10])`.
- You can also specify a step amount: `[1:10,2]`: `[1 3 5 7 9]`.
    - also works with floating point numbers: `[1:10,0.5]`.
- Or alternatively a fixed number of steps: `[0:10;5]`: `[0 2.5 5 7.5 10]`.

```python
@swim
def ramps(p=0.5, i=0):
    D('amencutup:[0:10]',
      room='[0:1,0.1]',
      cutoff='[1:10]*100', i=i)
    again(ramps, p=0.5, i=i+1)
```

