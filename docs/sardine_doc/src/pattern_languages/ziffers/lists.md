# Lists and operations

Integers can be arranged to lists for applying different operations.

```python
Pa * zd("superpiano","(0 1 2 3)-4") # Create a list and minus 4 from the items

Pa * zd("superpiano","(0 1 2 3)+<1 4 3>") # Create a list and cycle add operations

Pa * zd("superpiano","(0 1 2 3)+(1 2)") # Do a cartesian sum 0+1 0+2 1+1 1+2 2+1 2+2 3+1 3+2
```

# Assingment

List operations can be assigned to variables and played as a pattern

```python
Pa * zd("superpiano","A=(0 1 2) B=(4 2)+<4 2> A B A B B")
```

# Ranges and random values from list

```
Pa * zd('superpiano', '(0..7)')  # Create a list of 7
Pa * zd('superpiano', '(0..7)?4') # Pick random 4
Pa * zd('superpiano', '(0..7)~4') # Pick unique 4 (Suffle and pick first n)
```