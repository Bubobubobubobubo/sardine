# Numbers

## Integers and floating point numbers

The **Sardine Pattern Language** is supporting the same number types as Python:
- **integers:** `1`, `5`, `50012`.
- **floating point numbers:** `10.182`, `0.18`, `123.91239`.

All the common mathematical operators are also available and have their usual behavior:

```python
@swim
def number(p=0.5, i=0):
    print(P('1 1+1 1*2 1/3 1%4 1+(2+(5/2))', i))
    again(number, p=0.5, i=i+1)
```
**Parentheses** can be used for greater precision in the sequence of operations and to specify priority. The mathematical operators apply to numbers as well as to lists. You can for instance write an addition between a number and a list, between two lists, between a number and a note, between a chord and a list, etc..

```python
@swim
def number(p=0.5, i=0):
    print(P('C5 + 12', i))
    print(P('[10 20 30] + 2', i))
    again(number, p=0.5, i=i+1)
```

Many things can be safely considered as numbers such as **notes**. Internally, a **note** is also a number, whether it is a MIDI note number, a note inside a scale or any other mathematical representation.

## Random numbers

You can write random numbers by using the word `rand` or using the custom operators.
- `rand` will return a floating point number between `0.0` and `1.0`.
- `rand` will be casted to an **Integer** depending on the context (*e.g* `sample:r*8`).
- `rand` and `0.0~1.0` yield a similar result. Two ways to express the same idea.

There are multiple ways to generate randomness using Sardine. Even though `rand` is useful, 
using **time functions** will yield unpredictible results that are perceived by humans as randomness.
