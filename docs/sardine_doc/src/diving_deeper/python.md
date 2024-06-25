# Using Python
Sardine is written and executes in python. You can use python code both inside and outside of Players and @swim functions. This is one of most powerful features of Sardine - once you understand how to use it. There are also times where you need to execute python commands.

### Import modules
Importing modules is a standard way to access additional functionality in python. In Sardine, importing from the **random** module is needed whenever you want random values in your expressions or patterns. In the example there are two calls to random functions: `randint(100 ,400)` and `random(random()*1.5)+0.4`. `random()` generates a float between 0 and 1. Multipling this by 1.5 scales the random range out, and +0.4 moves it up, to avoid speeds that are too low.  This yields random values between `0.4 and 1.9`. 

```python
from random import * 
clock.tempo=90

@swim
def demo(p=1, i=0):
    D('electro1:2 electro1:4 electro1:3 feelfx:2',
    freq=randint(100,400),
    speed=(random() * 1.5) + 0.4,
    i=i)
    again(demo, p=0.5, i=i+1)
```

### Aliases
Looking for a way to reduce keystrokes? Aliases are simple. This example uses a python assignment with **a** as an alias for "again."

```python
a=again
@swim
def demo(p=1, i=0):
    D('electro1:2 electro1:4 electro1:3 feelfx:2', i=i)
    a(demo, p=0.5, i=i+1)
```

### Calling python functions
You can call python functions from within a @swim. The @swim below uses a Pattern Object to gradually increase and decrease the clock.tempo value. A python print() statement shows the value of clock.tempo as it is changing. 

```python
clock.tempo=90
@swim
def clockPat(p=1, i=0):
    print(f"clock.tempo: ", clock.tempo) # python print function
    clock.tempo=P('[90:180,2][180:90,4]', i) # Sardine Pattern Object
    again(clockPat, p=1, i=i+1)
```
### Generating values dynamically w custom functions
This shows a simple substitution. A variable is created with a string of note values. 
```python
seq = '40 51 62 72'
Pa * d('supersaw', n=seq)
```

Now instead of just setting fixed values, we write a short custom function to generate note values. Load the `lowHigh()` function first. Then start the **Pa** player. The same two notes will continue to play until you execute the Player again. This will cause it to make another function call to `lowHigh()`.

```python
def lowHigh():
    low = str(randint(30, 50))
    high = str(randint(50, 70))
    notes = low + ' ' + high
    return notes

Pa * d('supersaw', n=lowHigh()) # execute this line again to change note values
```

Custom functions can also be called within @swim, with an important difference. Here load the `lowHigh()` custom function then start the @swim. When referenced within the @swim, we get new note values every time! 

```python
def lowHigh():
    low = str(randint(30, 50))
    high = str(randint(50, 70))
    notes = low + ' ' + high
    return notes

@swim
def melody(p=1, i=0):
    D('supersaw', midinote=lowHigh(), i=i)
    again(melody, p=1, i=i+1)
```

### Conditional logic
This example uses python `if/elif/else` conditional logic to switch between sample sets and change the tempo. Notice the use of the iterator and how resetting it to 0 at the end resets the conditional logic. 

```python
@swim
def demo(p=1, i=0):
    print(f"i = ", i)
    if (i < 8):
        clock.tempo = 60
        D('electro1:2 electro1:4 electro1:3 feelfx:2', i=i)
    elif (i < 16):
        D('east:0~8', i=i)
        clock.tempo = 120
    else:
        i = 0
    again(demo, p=0.5, i=i+1)
```
### Going even deeper
See the next section - [Advanced python: Sample Slicer](./python-sampleslicer.md), where custom functions generate 4 Amphibian Variables at once. 
