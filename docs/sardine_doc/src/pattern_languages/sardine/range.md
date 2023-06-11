# Range

If you want to generate a number in the range `x` to `y` included, you can use the `~` operator. This operator will adapt to context (integer or floating point number). It can be used as an alternative to `rand` for scaled randomisation.

```python
@swim
def ranges(p=0.5, i=0):
    D('pluck|jvbass', speed='1~5', i=i)
    again(ranges, p=0.5, i=i+1)
```

People often forget about this one even though it is way shorter than `rand`.
