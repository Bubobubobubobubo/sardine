# Extend-Repeat

Use the `!!` operator to repeat each element of a list `x` times. Beware of the confusion with it's little brother, `!`. These two operators work hand in hand!

```python
@swim
def test_extend_repeat(p=0.5, i=0):
    D('pluck:19', legato=0.2,
    midinote='[60 62 63]!!3', i=i) #note the repetition of values within the list
    again(test_extend_repeat, p=0.125, i=i+1)
```
