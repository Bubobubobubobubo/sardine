# Patterning everything

You can use the `P()` object to get a generic interface to **Sardine** patterns. This object can be used just anywhere you would like to see a pattern. It means that you can contaminate your **Python** functions or anything in your code with them. Under the hood, **Sardine** patterns are spitting out valid **Python** integers, floats or strings.

```python
@swim
def free(p=0.5, i=0):
    print(P('1 2 3 4', i))
    again(free, p=0.5, i=i+1)
```
In the example above, we are just using a **swimming function** to print the result of a pattern in the interpreter window. Note that `P()` can take your basic iterator arguments as always (`P(pattern, iterator, divisor, rate)`.

We can do the same thing but using `P()` in a strategic location, replacing the static value for `p`:
```python
@swim
def free(p=0.5, i=0):
    D('cp')
    again(free, p=P('0.5!4 0.25!2', i), i=i+1)
```
Using this technique, you can easily generate rhythms or pattern data that you send to any **Python** function. Using `P()` is a good way to study **Sardine** patterns. You can just take a few minutes and study some specific patterns if you have a hard time understanding them. That&rsquo;s what I do sometimes when developping them :)

