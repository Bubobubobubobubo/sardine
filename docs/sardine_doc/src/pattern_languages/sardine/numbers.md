# Numbers

```python
@swim
def number(p=0.5, i=0):
    print(Pat('1 1+1 1*2 1/3 1%4 1+(2+(5/2))', i))
    again(number, p=0.5, i=i+1)
```

You can write numbers (both **integers** and **floating point numbers**) and use common operators such as addition, substraction, division, multiplication, modulo. Parentheses are supported. **Sardine** makes it so that most arithmetic operators can be used on anything expect if intuitively it doesn&rsquo;t make sense at all like multiplying a string against a string.

**You can apply arithmetic operators to numbers but also to lists!** You can for instance write an addition between a number and a list, between two lists, between a number and a note, between a chord and a list, etc..

Incidentally, it means that functions that work on lists can also work on single tokens. It also means that functions that are supposed to work for single numbers will work for lists, because the function will be mapped to every element in the list. **It turns the act of composing patterns into a rather interesting process.**

## Time-dependant numbers

```python
@swim
def number(p=0.5, i=0):
    # We print time-dependant values
    print(P('$ $.p $.m', i))
    again(number, p=0.5, i=i+1)
 ```   

Some number tokens are clock-time dependant (based on **Sardine** clock time).  Depending on the moment your loop/operation takes place, you might see some values recurring because you are not polling time continuously but at predictible rhythmic moments of time. Read that sentence twice, then read it again, **please**!
- `$`: **beat**, the current beat, with floating point precision.
- `$.p`: **phase**, a number between `0` and `1` denoting where you are in the beat.
- `$.m`: **measure**, the measure since the clock started.
    
```python
@swim
def number(p=0.5, i=0):
    print(Pat('$ $.m $.p', i))
    again(number, p=0.5, i=i+1)
```  
Some other number tokens are based on **absolute time**. They are not dependent on the clock. Use them for long-running sequences for introducing randomization. You will notice that they are all prefixed by `T`. `T` is a symbol very often associated with **time** in **Sardine**, while `$` denotes the clock time.
    
```python
@swim
def wow(p=0.5, i=0):
    print(Pat('T.U T.Y T.M T.D T.h T.m T.s T.µ', i))
    gain(wow, p=0.5, i=i+1)
```
    
- `T.U`: Unix Time, the current Unix Time.
- `T.Y`: year, the current year.
- `T.M`: month, the current month.
- `T.D`: day, the current day.
- `T.h`: hour, the current hour.
- `T.m`: minute, the current minute.
- `T.s`: second, the current second.
- `T.µ`: microsecond, the current microsecond.

## Random numbers

- You can write random numbers by using the word `rand`. `rand` will return a floating point number between `0.0` and `1.0`.
  -   In some contexts, `rand` will be casted to **Integer** if it makes more sense (context dependant, <span class="underline">e.g</span> `sample:r*8`).
- `rand` and `0.0~1.0` yield a similar result. Two ways to express the same idea.

## Patterns out of time

```python
@swim
def outof(p=0.25, i=0):
    D('cp', speed='$%10', i=i)
    again(outof, p=0.25, i=i+1)
```

Timed tokens make good **low frequency oscillators**, **ramps** or oscillating patterns. Playing with time tokens using modulos or the `sin()`, `cos()` or `tan()` functions is a great way to get generative results out of a predictible sequence.
- The faster you recurse (low `p`), the better your timing resolution is. You can start to enter into the realm of signal-like patterns that can be particularly good for generating fluid patterns. **Use this to generate fluid patterns.**


