# Logic

## AND (intersection)
Using `&&`, you can combine two lists using an element-wise AND.
If one of the operand is shorter than the other, it is repeated until it reaches the length of the longest one. Works best with 1s, 0s, and rests. For an element to appear in the result, it must be "truthy" in both lists. If either element is "falsy", the result for that position will be "falsy".

```python
Pa * d('(set pk [1 . . .]) * kick')
Pb * d('(set ps [.!4 1 .!2 1]) * sd')
Pd * d('(get pk) && (get ps) * bleep')  # outputs [.... 1 ...]
```

## OR (union)
Using `||`, you can combine two lists using an element-wise OR. 
If one of the operand is shorter than the other, it is repeated until it reaches the length of the longest one. If either element is "truthy", the result for that position will be "truthy". Only if both elements are "falsy" will the result be "falsy".

```python
Pa * d('(set pk [1 . . .]) * kick')
Pb * d('(set ps [.!4 1 .!2 1]) * sd')
Pd * d('(get pk) || (get ps) * bleep')  # outputs [1 ... 1 .. 1]
```

## XOR (exclusive disjunction)
Using `^|`, you can combine two lists using an element-wise XOR (exclusive OR).
If one of the operand is shorter than the other, it is repeated until it reaches the length of the longest one. If exactly one element is "truthy" and the other is "falsy", the result will be "truthy". If both elements are "truthy" or both are "falsy", the result will be "falsy".

```python
Pa * d('(set pk [1 . . .]) * kick')
Pb * d('(set ps [.!4 1 .!2 1]) * sd')
Pd * d('(get pk) ^| (get ps) * bleep')  # outputs [1 ...... 1]
```
