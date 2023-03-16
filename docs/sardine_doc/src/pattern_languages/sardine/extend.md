# Extend

- you can extend a list by calling the `!` operator on it. 
  - This will repeat the list x times.

```python
@swim
def test_extend(p=0.5, i=0):
    D('pluck:19', legato=0.2, midinote='[60 62]!2', i=i)
    again(test_extend, p=0.125, i=i+1)
```
