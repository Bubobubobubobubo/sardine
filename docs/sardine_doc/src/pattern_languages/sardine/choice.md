# Choice

The pipe operator `|` can be used on anything to make a 50/50%
choice between two tokens. You can also chain them: `1|2|3|4`.
The behavior of chaining multiple choice operators has not been 
clearly defined. The distribution might not be the one you expect.

```python
@swim
def choosing stuff(p=0.5, i=0):
    D('bd|pluck', speed='1|2', i=i)
    again(choosing_stuff, p=0.5, i=i+1)
```


