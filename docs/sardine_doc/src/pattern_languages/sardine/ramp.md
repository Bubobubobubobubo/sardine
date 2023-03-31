# Ramp

    
- This operator is very reminiscent of the **range()** function, only better.
- You can generate ramps of integers using the `[1:10]` syntax.
    - This expression will yield `[1 2 3 4 5 6 7 8 9 10]`.
- You can ramp up and you can ramp down!
- You can be more specific: `[1:10,2]`.
    - This expression will yield: `[1 3 5 7 9]`.
    - It also works with floating point numbers and floating point number steps: `[1:10,0.5]`!

```python
@swim
def ramps(p=0.5, i=0):
    D('amencutup:[0:10]',
      room='[0:1,0.1]',
      cutoff='[1:10]*100', i=i)
    again(ramps, p=0.5, i=i+1)
```
