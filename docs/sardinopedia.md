---
hide:
    - navigation
---

The Sardinopedia is a growing collection of interesting **Sardine** patterns. Patterns worthy of inclusion in the Sardinopedia must at least possess one of the following qualities:

- **they are demonstrative**: they demonstrate something made possible by **Sardine**.

- **they are didactic**: they teach you how to use **Sardine**.

- **they are musical**: they have an interesting musical result.

- **they are odd**: they show something odd, unexpected, funny, etc...


## Basic (Swimming lessons)

This section will help you to grow more confident with *swimming functions*. They must dance before your eyes like a group of sardines swimming in the ocean. They are not really elegant Python code. It's better to be acustomed to using them before attempting to play live.

### Swimming

```python3
@swim # or @die
def basic():
    print('I am swimming now!')
    again(basic)

hush(basic)
```
The most basic function you can write.

### Swimming with style

```python3
@swim 
def basic(d=0.5, i=0):
    print('I am swimming now!')
    again(basic, d=0.5, i=i+1)

hush(basic)
```
The most common function. A function with a duration and an iterator passed as argument.


### Drowning in numbers

```python3
@swim 
def basic(d=0.5, i=0, j=0, k=0):
    print('I am swimming now!')
    again(basic, d=0.5, i=i+1, j=i+2, k=P('r*10', i))

hush(basic)
```
A function with three different iterators. Why not?

### Swimming with friends

```python3
def calling_you():
    print("I hear you")

@swim 
def basic():
    calling_you()
    again(basic)

hush(basic)
```
Calling a regular function from a swimming function.

### Synchronized Swimming

```python3
@swim
def first():
    print('first!')
    again(second)
def second():
    print('second!')
    again(first)
```
A swimming function calling another one, calling back the first.

### Waterpolo

```python3
@swim
def first(d=0.5, rng=0):
    print(f"Received: {rng}")
    rng = randint(1,10)
    print(f"Sending: {rng}")
    again(second, d=0.5, rng=rng)

# evaluate me first
def second(d=0.5, rng=0):
    print(f"Received: {rng}")
    rng = randint(1,10)
    print(f"Sending: {rng}")
    again(first, d=0.5, rng=rng)
```
Feeding one swimming function with the data of another.

## Sound (SuperDirt)

### Bassdrum

```python3
def bd(d=0.5):
    S('bd').out()
    again(bd, d=0.5)
```
A simple bassdrum playing every 2 beats.

### Bassdrum fun

```python3
def bd(d=0.5):
    S('bd', speed='r*4', legato='r', cutoff='100+(r*4000)').out()
    again(bd, d=0.25)
```
A simple bassdrum but some parameters have been tweaked to be random.

### Breakbeat

```python3
def bd(d=0.5, i=0):
    S('amencutup:r*20').out(i)
    again(bd, d=0.25, i=i+1)
```
Picking a random sample in a folder containing the amen break. You could have a successful career doing this in front of audiences.

### Sample sequence

```python3
def bd(d=0.5, i=0):
    S('bd,hh,sn,hh').out(i)
    again(bd, d=0.5, i=i+1)
```
Your classic four on the floor written on one line.


## Rhythm

### Probability rhythms

```python3
def bd(d=0.5):
    if often():
        S('bd').out()
    if sometimes():
        S('hh).out()
    else:
        S('pluck').out()
    # condensed 
    S('sd', trig=1 if sometimes() else 0).out()
    again(bd, d=0.5)
```

Building rhythms based on chance that an event will happen. Rolling a dice.

### Binary rhythm

```python3
def bd(d=0.5, i=0):
    S('bd', trig=bin(20103)).out(i)
    again(bd, d=0.5, i=i+1)
```
Using the binary representation of a number to build a rhythm. You don't need to know what the representation is to get an interesting rhythm out of it.

### Euclidian rhythms

```python3
def bd(d=0.5, i=0):
    S('bd:r*20', trig=euclid(1,4)).out(i)
    S('hh:r*20', trig=euclid(6,8)).out(i)
    S('sd:r*20', trig=euclid(2,4)).out(i)
    again(bd, d=0.5, i=i+1)
```
Building euclidian rhythms by using the `trig` argument. Note that this is not really an euclidian rhythm but it sure does look and feel like it. Trig allows you to skip an event.

### Shifting rhythm

```python3
def bd(d=0.5, i=0):
    S('bd:r*20', trig=euclid(1,4)).out(i)
    S('hh:r*20', trig=euclid(6,8)).out(i)
    S('sd:r*20', trig=euclid(2,4)).out(i)
    again(bd, d=P('0.5!8, 0.25!4', i), i=i+1)
```
Pattern the recursion delay to get free rhythms! You can even skip playing with `trig` and just play with the recursion `delay` if you feel like it!

## Pitch

### Playback speed

```python3
def hh(d=0.5, i=0):
    S('hh', speed='{1_8}').out(i)
    again(hh, d=P('0.5!8, 0.25!4', i), i=i+1)
```
Changing the speed of audio playback for a given audio sample. Cheap version of tuning.

### Sample to pitch

```python3
def hh(d=0.5, i=0):
    S('hh', midinote='C5!3, E5, G5').out(i)
    again(hh, d=P('0.5!8, 0.25!4', i), i=i+1)
```
Pitching an audio sample relatively to a MIDI note.

## Texture
