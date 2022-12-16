## Rhythm

### Probability rhythm

```python3
@swim
def bd(p=0.5):
    if often():
        D('bd')
    if sometimes():
        D('hh')
    else:
        D('pluck')
    # condensed
    D('sd', trig=1 if sometimes() else 0)
    again(bd, p=0.5)
```

Building rhythms based on chance that an event will happen. Rolling a dice. These small functions are borrowed from **TidalCycles** that is using them intensively in its very thorough patterning system.

### Binary rhythm

```python3
@swim
def bd(p=0.5, i=0):
    D('bd', trig=bin(20103), i=i)
    again(bd, p=0.5, i=i+1)
```
Using the binary representation of a number to build a rhythm. You don't need to know what the representation is to get an interesting rhythm out of it. Feed anything to the `bin` function and get something out!

### Euclidian rhythm

```python3
@swim
def bd(p=0.5, i=0):
    D('bd:r*20', trig=euclid(1,4), i=i)
    D('hh:r*20', trig=euclid(6,8), i=i)
    D('sd:r*20', trig=euclid(2,4), i=i)
    again(bd, p=0.5, i=i+1)
```
Building euclidian rhythms by using the `trig` argument. Note that this is not really an euclidian rhythm but it sure does look and feel like it. Trig allows you to skip an event.

### Shifting rhythm

```python3
@swim
def bd(p=0.5, i=0):
    D('bd:r*20', trig=euclid(1,4), i=i)
    D('hh:0~5', trig=euclid(6,8), i=i)
    D('sd:$%20', trig=euclid(2,4), i=i)
    again(bd, p=P('0.5!8, 0.25!4', i), i=i+1)
```
Pattern the recursion delay to get free rhythms! You can even skip playing with `trig` and just play with the recursion `delay` if you feel like it!

### Imperative rhythm

```python3
@swim
def zoom(p=0.5, i=0):
    D('bd:r*20', i=i)
    sleep(0.25)
    D('hh:r*20', trig=euclid(6,8), i=i)
    sleep(0.125)
    D('sd:r*20', trig=euclid(2,4), i=i)
    again(zoom, p=0.5, i=i+1)
```
Create rhythm using the `sleep()` function. Fully compatible with everything else! It is usually a good idea to use `sleep()` after having composed something complex to slice time even more.

### Silence rhythms

```python3
@swim
def silence_rhythm(p=0.5, i=0):
    D('bd', i=i, d=4)
    D('hh:2', i=i, d=2)
    D('drum:2+r*5', i=i, d=3)
    a(silence_rhythm, p=1/8, i=i+1)
```

Play with the `divisor` amount to generate interesting rhythms.
