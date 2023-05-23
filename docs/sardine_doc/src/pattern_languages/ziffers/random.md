# Random values

Random values can be generated using *?* or *(n,n)* syntax:

```python
Pa * zd('superpiano', 'q 0 ? 3 ? 5') # Random within the scale (0-last scale degree)
Pa * zd('superpiano', 'q 0 (1,4) 5 (6,8)') # Random within a range
```