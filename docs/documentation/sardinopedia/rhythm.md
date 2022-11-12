## Rhythm

### Probability rhythm

```python3
@swim
def bd(d=0.5):
    if often():
        S('bd').out()
    if sometimes():
        S('hh').out()
    else:
        S('pluck').out()
    # condensed 
    S('sd', trig=1 if sometimes() else 0).out()
    again(bd, d=0.5)
```

Building rhythms based on chance that an event will happen. Rolling a dice. These small functions are borrowed from **TidalCycles** that is using them intensively in its very thorough patterning system.

### Binary rhythm

```python3
@swim
def bd(d=0.5, i=0):
    S('bd', trig=bin(20103)).out(i)
    again(bd, d=0.5, i=i+1)
```
Using the binary representation of a number to build a rhythm. You don't need to know what the representation is to get an interesting rhythm out of it. Feed anything to the `bin` function and get something out!

### Euclidian rhythm

```python3
@swim
def bd(d=0.5, i=0):
    S('bd:r*20', trig=euclid(1,4)).out(i)
    S('hh:r*20', trig=euclid(6,8)).out(i)
    S('sd:r*20', trig=euclid(2,4)).out(i)
    again(bd, d=0.5, i=i+1)
```
Building euclidian rhythms by using the `trig` argument. Note that this is not really an euclidian rhythm but it sure does look and feel like it. Trig allows you to skip an event.

### Shifting rhythm

```python3
@swim
def bd(d=0.5, i=0):
    S('bd:r*20', trig=euclid(1,4)).out(i)
    S('hh:0~5', trig=euclid(6,8)).out(i)
    S('sd:$%20', trig=euclid(2,4)).out(i)
    again(bd, d=P('0.5!8, 0.25!4', i), i=i+1)
```
Pattern the recursion delay to get free rhythms! You can even skip playing with `trig` and just play with the recursion `delay` if you feel like it!

### Imperative rhythm

```python3
@swim
def zoom(d=0.5, i=0):
    S('bd:r*20').out(i)
    sleep(0.25)
    S('hh:r*20', trig=euclid(6,8)).out(i)
    sleep(0.125)
    S('sd:r*20', trig=euclid(2,4)).out(i)
    again(zoom, d=0.5, i=i+1)
```
Create rhythm using the `sleep()` function. Fully compatible with everything else! It is usually a good idea to use `sleep()` after having composed something complex to slice time even more.

### Silence rhythms

```python3
@swim 
def silence_rhythm(d=0.5, i=0):
    S('bd').out(i, div=4)
    S('hh:2').out(i, div=2)
    S('drum:2+r*5').out(i, div=3)
    a(silence_rhythm, d=1/8, i=i+1)
```

Play with the `div` amount to generate interesting rhythms.


