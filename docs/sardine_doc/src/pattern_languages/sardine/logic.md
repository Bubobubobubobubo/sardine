# Logic


## AND (union)
Using `&&`, you can combine two lists using an element-wise AND.
If one of the operand is shorter than the other, it is repeated until it reaches the length of the longest one. Works best with 1s, 0s, and rests. If two "falsy" or two "truthy" elements are being compared, the one from the left operand is kept, otherwise the "falsy" element among the two is kept.

```python
Pa * d('(set pk [1 . . .]) * kick')
Pb * d('(set ps [.!4 1 .!2 1]) * sd')
Pd * d('(get pk) && (get ps) * bleep')  # outputs [1 ... 1 .. 1]
```

## OR (intersection)
Using `||`, you can combine two lists using an element-wise OR. If two "falsy" elements are being compared, the one from the left operand is kept, otherwise, the leftmost "truthy" is kept.

```python
Pa * d('(set pk [1 . . .]) * kick')
Pb * d('(set ps [.!4 1 .!2 1]) * sd')
Pd * d('(get pk) || (get ps) * bleep')  # outputs [.... 1 ...]
```

## OR (exclusive disjunction)
Using `^|`, you can combine two lists using an element-wise OR. If two "truthy" or two "falsy" elements are being compared, a rest is returned, otherwise the truthy element is returned.

```python
Pa * d('(set pk [1 . . .]) * kick')
Pb * d('(set ps [.!4 1 .!2 1]) * sd')
Pd * d('(get pk) ^| (get ps) * bleep')
```

