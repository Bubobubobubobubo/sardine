# Period - Divisor - Rate
Period, Divisor and Rate all impact how rhythm is expressed in Sardine. Period is the most important and has the most flexibility. Divisor and rate have a more narrow focus, but can be used effectively particularly in combination with period. 

## Period
Period determines the number of steps per beat. (Beat is set by the `clock.tempo` value in BPM.) Period has a default value of 1 and often set to values less than one to subdivide the beat. Setting `p=0.5` sets the period to half of the beat (notes will be twice as fast). `p=2` sets the period to twice the length of the beat (notes will be twice as slow). 

It is common to use regular values of p, such as 0.5, 0.25. But period can be set to any value, including fractions and decimals. This can result in rhythms that don't line up on the beats, polyrhythms, or granular synthesis like effects when very low period values (0.05 or less) are used.

### Period with Players
To understand how period works, consider the set of Players below. The clock is set to 60 BPM to give a slower tempo and make everything clear. Keep the first pattern playing to serve as a metronome. Add each player individually and notice what the different period values do. 

```python
clock.tempo=60
Pa * d('hh27:2', p=1)   # one note per beat - use as a metronome

Pb * d('hh:10',  p=0.5) # subdivides beat
Pc * d('hh:4',   p=2)   # every other beat
Pd * d('hh:9',   p=1/3) # triplet subdivision
Pe * d('hh:2 . hh:2', p=0.268) #irregular subdivision 
Pf * d('hh:5',   p='1!2 0.5!2 0.25!4') # period pattern
```
Notice the use of a pattern value for period in the **Pf** player `p='1!2 0.5!2 0.25!4'`. The pattern means that Sardine will change the period value on each repeat. This creates rhythm. Try changing the pattern to see how the rhythm changes. 

### Period in @swim functions
Period also works in @swim functions with some differences. Most importantly, the period value is set for the **whole** @swim function and is not set in each Sender. Also, to use a pattern with the period value the Pattern Object is required. 

The example below translates the Players above into @swim functions. Notice that we can't contain all 5 players in a single @swim function because we can't set a unique period value in each Sender. The period needs to be set as an argument in the `again()` statement. 

```python
clock.tempo=60
@swim
def demo1(p=1, i=0):
    D('hh27:2', i=i)
    D('hh:4', d=2, i=i) # divisor set to 2
    again(demo1, p=1, i=i+1)

@swim
def demo2(p=1, i=0):
    D('hh:9', i=i) 
    again(demo2, p=1/3, i=i+1)

@swim
def demo3(p=1, i=0):
    D('hh:5!2 hh:11', i=i) 
    again(demo3, p=P('1!2 0.5!2 0.25!4', i), i=i+1) # P() is the Pattern Object
```

### Pattern Object
The **demo3** function above introduces the Pattern Object.  

- `p=P('<pattern value sequence>', i)` `p=P('1!2 0.5!2 0.25!4', i)`
- Within the quotes, any valid pattern can be used. 

The Pattern Object provides an iterator value within the again() statement. If you leave off the P('') and just put a pattern, Sardine will throw an error. For more information see [Diving Deeper > Patterning everything](../diving_deeper/patterning_everything.md).

### Period with random values
Periods can be randomized but will behave differently in Player and @swim. Note that you first need to import the random functions in python. In the **Pa** player below, a random decimal value between 0 and 2 will be generated the first time it is called. But in a Player, the value assigned to the period will stay the same until you re-execute the Player code line. 

In @swim, the random call will happen automatically on every iteration, making the period value change on every beat. This has an unsual effect musically where the rhythm becomes irregular. 

```python
from random import *
Pa * d('hh27:2', p=random()*2)

@swim
def demoR(p=1, i=0):
    D('hh27:2', i=i)
    D('hh:4', d=2, i=i) 
    again(demoR, p=random()*2, i=i+1)
```

## Divisor
Divisor is a way of controlling the number of beats per note. Think of it as dividing the step so that multiple beats occur before the next step. Divisors are expressed as integer values. These will slow the pattern down and stretch it out. It can be helpful to use this in combination with faster period values. 

Syntax

| Player | @swim  | Notes     |
|:------:|:------:|:----------|
| `d=2` or `divisor=2` | `d=2` | "d" is most common  |
| argument in sender | (same)  | in @swim divisor can be set independantly in each sender |

- use integers: 1, 2, 3, 4 ... 

Adding a divisor together with a period in a single player may seem like they would cancel each other out. But higher divisor values can be used to create offbeat rhythms. With irregular or patterned periods, a divisor is an effective way to preserve the period but stretch it out. 

```python
clock.tempo=60
Pa * d('hh27:2', p=1) # play as metronome

# try the different values for d and p
Pb * d('hh:10', p=0.5, d=1) # start here d=1
Pb * d('hh:10', p=0.5, d=2) # changes divisor to 2
Pb * d('hh:10', p=0.25, d=2) # lowers period to 0.25 - notice the offbeat rhythm
```

Divisors can also be used to preserve an irregular period value but extend it and slow it down.
```python
clock.tempo=60
Pa * d('hh27:2', p=1) # play as metronome

# try the different values for d and p
Pe * d('hh:2 . hh:2', p=0.268, d=1)
Pe * d('hh:2 . hh:2', p=0.268, d=3) # preserves the period value but slows it down

Pf * d('hh:5', p='1!2 0.5!2 0.25!4', d=1)
Pf * d('hh:5', p='1!2 0.5!2 0.25!4', d=2) # slows the pattern down
```

### Divisor in @swim 
When using multiple senders, divisors let you set and change the rhythmic pace independantly for each sender. This can be useful for having different patterns execute at different rates. Note how each sender below has a different divisor value. This works well with a low period setting `p=0.25`.

```python
@swim
def demoDiv(p=1, i=0):
    D('hh27:2', d=2, i=i)
    D('hh:4', d=3, i=i) 
    D('hh:9', d=4, i=i) 
    D('hh:3 . hh:3!2', d=1, i=i) 
    D('hh:2 . . hh:2', d=5, i=i) 
    D('. . alphabet:6', d=6, i=i) 
    again(demoDiv, p=0.25, i=i+1)
```

## Rate
The **rate** argument is used in Senders and works the same for Players and @swim. The rate value is applied to a pattern and controls the rate at which the iterator cycles through pattern changes. With values less than 1, the rate of change is slower, resulting in more repetition within the pattern. For example, with `rate=0.5`, each value in a pattern will repeat twice. 

Try the different values on the same players below, and see how different rate values change the output. 

```python
clock.tempo=120
Pa * d('hh27:5 hh27:2 hh27:1 hh27:6 hh:9', p=0.5, rate=1)
Pa * d('hh27:5 hh27:2 hh27:1 hh27:6 hh:9', p=0.5, rate=0.5)
Pa * d('hh27:5 hh27:2 hh27:1 hh27:6 hh:9', p=0.38, rate=0.85)

Pb * d('hh:0~12', p=0.5, rate=1)
Pb * d('hh:0~12', p=0.5, rate=0.5)
Pb * d('hh:0~12', p=0.5, rate=0.25)

@swim
def demoDiv(p=1, i=0):
    D('hh27:2 hh27:9 hh27:1', d=2, rate=0.5, i=i)
    D('hh:4 hh:9', d=3, rate=0.2, i=i) 
    D('. reverbkick', d=5, i=i)
    again(demoDiv, p=0.5, i=i+1)
```
Here is an example of period, divisor, and rate working in combination to create an unusual result.

```python
TBD - Bubo, can you add something here? 
```
