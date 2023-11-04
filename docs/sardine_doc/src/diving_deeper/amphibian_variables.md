# Amphibian Variables

```python
from random import random
V.s = 60 # this is an amphibian variable

@swim
def fun():
    # Calling the variable from inside the Sardine Pattern Language
    N('(getA s)')
    if random() > 0.8:
        V.s = random() * 80 # setting a random value
    again(fun)
```

- There are variables called **amphibian variables**. They are both valid inside and outside the pattern notation.
- They are defined using the variable `V` followed by a letter from the alphabet (uppercase or lowercase) : `V.a`, `V.A`, `V.Z`, `V.j`. These variables can be freely manipulated from the Python side or from the pattern side. **They are amphibian because they exist in the two languages**.

Here is how you manipulate them:
- The `(getA letter)` function can access an amphibian variable from inside the pattern language. 
- The `(setA letter value)` function can set an amphibian variable from inside the pattern language.
    
```python
@swim
def fun(p=0.25):
    # Now having fun with it
    N('(setA s 5~80)') # setting a random value to the variable
    if random() > 0.8:
        v.s = 50
    again(fun, p=0.25)
```

Amphibian Variables also work in Players:
```python

V.n = [52, randint(40, 60), 72, 35]
Pa * d('supersaw', n='(getA n)', p=0.75 )
```

You can use Amphibian Variables to leverage Python or the pattern syntax for what they do best: patterning or dealing with complex algorithmic transformations. Having them both available makes the pattern syntax even more expressive.

For more exploration of Amphibian Variables, see:
- [Using Python](./python.md)
- [Advanced Python: Sample Slicer](./python-sampleslicer.md)
