---
hide:
    - navigation
---

The Sardinopedia is a growing collection of interesting **Sardine** patterns. Patterns worthy of inclusion in the Sardinopedia must at least possess one of the following qualities:

- **they are demonstrative**: they demonstrate something made possible by **Sardine**.

- **they are didactic**: they teach you how to use **Sardine**.

- **they are musical**: they have an interesting musical result.

- **they are odd**: they show something odd, unexpected, funny, etc...

## Demonstration patterns

These patterns are small songs and/or long patterns that you can copy and paste to familiarise yourself with the syntax. Change some values, comment a few lines here and there. Try to learn how to move and alter **Sardine** code.


## Basic (Swimming lessons)

This section will help you to grow more confident with *swimming functions*. They must dance before your eyes like a group of sardines swimming in the ocean. They are not really elegant Python code. It's better to be acustomed to using them before attempting to play live.

### Out-of-time

```python3
S('bd').out()
```
You can use the Sender objects outside of every function. It will work, but you will be un-timed or out-of-time. This technique can be used to trigger long samples, FXs, etc... It can also be used to change (non-periodcally) some values on your MIDI synthesizers or OSC receivers.

### Swimming

```python3
@swim # or @die
def basic():
    print('I am swimming now!')
    again(basic)

hush(basic)
```
The most basic function you can write. This is the skeleton of a *swimming function*. You will encounter it everytime you play with **Sardine**.

### Swimming with style

```python3
@swim 
def basic(d=0.5, i=0):
    print('I am swimming now!')
    again(basic, d=0.5, i=i+1)

hush(basic)
```
The most common function. A function with a duration and an iterator passed as argument. This is the one you should save as a snippet somewhere in your text editor.


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

## Senders

### Bassdrum (S)

```python3
@swim
def bd(d=0.5):
    S('bd').out()
    again(bd, d=0.5)
```
A simple bassdrum playing every 2 beats.

### Bassdrum fun (S)

```python3
@swim
def bd(d=0.5):
    S('bd', speed='r*4', legato='r', cutoff='100+(r*4000)').out()
    again(bd, d=0.25)
```
A simple bassdrum but some parameters have been tweaked to be random.

### Breakbeat (S)

```python3
@swim
def bd(d=0.5, i=0):
    S('amencutup:r*20').out(i)
    again(bd, d=0.25, i=i+1)
```
Picking a random sample in a folder containing the amen break. You could have a successful career doing this in front of audiences.

### Sample sequence (S)

```python3
@swim
def bd(d=0.5, i=0):
    S('bd,hh,sn,hh').out(i)
    again(bd, d=0.5, i=i+1)
```
Your classic four-on-the-floor written on one line.

### Piling up samples (S)

```python3
@swim
def pluck(d=0.5, i=0):
    S('pluck').out(i)
    S('pluck:1').out(i)
    S('pluck:2').out(i)
    S('pluck:3').out(i)
    again(pluck, d=0.5, i=i+1)
```
You can stack events without waiting. They will be sent immediately.

### MIDI Note (M)

```python3
@swim
def midi(d=0.5, i=0):
    M().out()
    again(midi, d=0.5, i=i+1)
```
No argument is enough to send a MIDI Note (60) at full velocity (127) on the first default MIDI channel. Arguments are only used to specify further or to override default values.

### MIDI Tune (M)

```python3
@swim
def midi(d=0.5, i=0):
    M(note='C5,D5,E5,G5,E5,D5,G5,C5').out(i)
    again(midi, d=0.5, i=i+1)
```
Playing a little melody by tweaking the `note` argument.

### Full MIDI Tune (M)

```python3
@swim
def midi(d=0.5, i=0):
    M(channel='0,1,2,3',
      velocity='20 + (r*80)',
      note='C5,D5,E5,G5,E5,D5,G5,C5').out(i)
    again(midi, d=0.5, i=i+1)
```
The same melody spreaded out on three MIDI channels (one per note) with random velocity.

### Other messages (M)

```python3
@swim
def midi(d=0.5, i=0):
    M(channel='0,1,2,3',
      velocity='20 + (r*80)',
      note='C5,D5,E5,G5,E5,D5,G5,C5').out(i)
    pgch(P('1,2,3,4', i)) # switching
    cc(channel=0, control=20, value=50) # control
    again(midi, d=0.5, i=i+1)
```
Switching between program `1`, `2`, `3` and `4` on your MIDI Synth. Sending a control change on channel `0`, number `20` for a value of `50`.



## Rhythm

### Probability rhythm

```python3
@swim
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
@swim
def bd(d=0.5, i=0):
    S('bd', trig=bin(20103)).out(i)
    again(bd, d=0.5, i=i+1)
```
Using the binary representation of a number to build a rhythm. You don't need to know what the representation is to get an interesting rhythm out of it.

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
    S('hh:r*20', trig=euclid(6,8)).out(i)
    S('sd:r*20', trig=euclid(2,4)).out(i)
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


## Pitch

### Playback speed

```python3
@swim
def hh(d=0.5, i=0):
    S('hh', speed='{1_8}').out(i)
    again(hh, d=0.5, i=i+1)
```
Changing the speed of audio playback for a given audio sample. Cheap version of tuning.

### Sample to pitch

```python3
@swim
def hh(d=0.5, i=0):
    S('hh', midinote='C5!3, E5, G5').out(i)
    again(hh, d=0.5, i=i+1)
```
Pitching an audio sample relatively to a MIDI note.

### Sample to freq

```python3
@swim
def hh(d=0.5, i=0):
    S('hh', freq='100 + (r*2000)').out(i)
    again(hh, d=0.5, i=i+1)
```
Pitching an audio sample relatively to a given frequency (in `hertz`).

## Texture and effects


## Patterning basics

### Patterning freely (P)

```python3
@swim
def free(d=0.5, i=0):
    # Look at P
    print(P('1,2,3,4', i))
    again(free, d=0.5, i=i+1)
```
`P()` is an interface to the patterning system. Write a pattern between quotation marks (`''` or `""`) and get something back. You will need to feed the pattern system a value to extract an index (`i`).

### Patterning in Senders (P)

```python3
@swim
def boom(d=0.5, i=0):
    S('bd', 
        cutoff='r*2000',
        speed='1,2,3,4').out(i)
    again(boom, d=0.5, i=i+1)
```
Sender objects are automatically turning string arguments into patterns. Feed the index value to the `.out()` method.

### Patterning using both methods (P)

```python3
@swim
def boom(d=0.5, i=0):
    S('bd', 
        cutoff=P('r*2000', i),
        speed='1,2,3,4').out(i)
    again(boom, d=0.5, i=i+1)
```
The result of this *swimming function* is strictly similar to the one directly above. Notice the difference in coding style, with the usage of `P()`.

### See me change (P)

```python3
@swim
def boom(d=0.5, i=0):
    S('bd', 
        cutoff=P('r*2000', i),
        speed='1,2,3,4').out(i)
    again(boom, d=0.5, i=i+1 if random() > 0.5 else -1)
```
Playing around with the basic `i` iterator structure.

### Index madness (P)

```python3
@swim
def boom(d=0.5, i=0):
    S('bd', 
        cutoff=P('r*2000, 500, 1000', i%2),
        speed='1,2,3,4').out(randint(1,4))
    again(boom, d=0.5, i=i+1)
```
You can be creative with pattern indexes and get random sequences, drunk walks, reversed sequences, etc... Be sure to always have a few different iterators close by to morph your sequences really fast.

## Pattern syntax

This section is very likely to change in upcoming versions.

### Numbers

```python3
@swim
def number(d=0.5, i=0):
    print(P('1, 1+1, 1*2, 1/3, 1%4, 1+(2+(5/2))')).out(i)
    again(number, d=0.5, i=i+1)
```
You can write numbers and use common operators such as addition, substraction, division, multiplication, modulo, etc... You can be specific about priority by using parenthesis.

### Time tokens

```python3
@swim
def number(d=0.5, i=0):
    print(P('$, r, m, p')).out(i)
    again(number, d=0.5, i=i+1)
```
Some number tokens are time dependant (based on **Sardine** clock time) and refer to a moment in time. Depending on the moment where your recursion takes place, you might see some values recurring because you are not polling continuously but polling just a predictible moment in time. 

- `$`: tick, the tick number since the clock started.
- `r`: random, between `0` and `1`.
- `p`: phase, a number between `0` and your `c.ppqn`.
- `m`: measure, the measure since the clock started.

```python3
@swim
def number(d=0.5, i=0):
    print(P('r, m, p')).out(i)
    again(number, d=0.5, i=i+1)
```

Some number tokens are time dependant, but will refer to absolute time. They are mostly used for long-running sequences and/or for introduction a random factor in your computation. You will notice that they are prefixed by `$`.
```python3
@swim
def random(d=0.5, i=0):
    print(P('$.Y, $.M, $.D, $.H, $.m, $.S, $.µ', i))
    again(random, d=0.5, i=i+1)
```

- `$.Y`: year, the current year.
- `$.M`: month, the current month.
- `$.D`: day, the current day.
- `$.H`: hour, the current hour.
- `$.m`: minute, the current minute.
- `$.S`: second, the current second.
- `$.µ`: microsecond, the current microsecond.

### Timed maths

```python3
@swim
def random(d=0.5, i=0):
    S('cp', speed='$%20').out(i)
    again(random, d=0.5, i=i+1)
```
Timed tokens make good low frequency oscillators or random values for generating interesting patterns. Playing with time tokens is a great way to get generative results out of a predictible sequence.

### Notes

```python3
@swim
def notes(d=0.5, i=0):
    S('pluck', midinote='C5,D5,E5,F5,G5').out(i)
    again(notes, d=0.5, i=i+1)
```
You can write notes in patterns. Notes will be converted to some MIDI value used by **SuperDirt**. It means that notes are numbers too and that you can do math on them if you wish to. The syntax to write notes is the following. The steps 2 and 3 can be omitted:

- 1) capital letter indicating the note name: `C`,`D`,`E`,`F`,`G`,`A`,`B`
- 2) flat or sharp: `#`, `b` 
- 3) octave number: `0`..`9` 

### Note qualifiers

```python3
@swim
def notes(d=0.5, i=0):
    S('pluck', midinote='C5->penta').out(i)
    again(notes, d=0.5, i=i+1)
```
Use the `print_scales()` function to print out the list of possible scales, chords and structures you can play with. You can use the `->` to **qualify** a note, to summon a collection of notes or a structure based on the provided note. `C->penta` will raise a major pentatonic scale based on middle C.

### Note modifiers

```python3
@swim
def notes(d=0.5, i=0):
    S('pluck', midinote='C5->penta.disco.braid').out(i)
    again(notes, d=0.5, i=i+1)
```
Some modifiers are available to fine-tune your note collections. There is currently no way to print out the list of `modifiers`. You will have to deep-dive in the source code to find them.

### Note maths

```python3
@swim
def notes(d=0.5, i=0):
    S('pluck', midinote='C5+0|4|8->penta.disco.braid').out(i)
    again(notes, d=0.5, i=i+1)
```
You can use arithmetic operators on notes.

### Names

```python3
@swim
def names(d=0.5, i=0):
    S('bd, pluck, bd, pluck:2+4').out(i)
    again(names, d=0.5, i=i+1)
```
You are using name patterns since you first started! You can also pattern names. The whole pattern syntax works just the same.

### Addresses

### Choice 

```python3
@swim
def choosing_stuff(d=0.5, i=0):
    S('bd|pluck', speed='1|2').out(i)
    again(choosing_stuff, d=0.5, i=i+1)
```
The pipe operator `|` can be used to make a 50/50% choice between two tokens. You can also chain them: `1|2|3|4`.

### Ranges

```python3
@swim
def ranges(d=0.5, i=0):
    S('pluck|jvbass', speed='1:5').out(i)
    again(ranges, d=0.5, i=i+1)
```
If you want to generate a number in the range `x` to `y` included, you can use the `:` operator.

### Ramps

```python3
@swim
def ramps(d=0.5, i=0):
    S('amencutup:{0_10}', 
        room='{0_1(0.1)}',
        cutoff='{1_10}*100').out(i)
    again(ramps, d=0.5, i=i+1)
```

You can generate ramps using the `{1_10}` syntax. This will generate the following list: `[1, 2, 3, 4, 5, ..., 10]`. You can generate lists ramping up and down. You can also generate a ramp with a floating point range by specifying it in-between parentheses: `{1_10(10)}`.

### Repeat

```python3
@swim
def repeat_stuff(d=0.5, i=0):
    S('pluck|jvbass', speed='1:2', midinote='C4!4, E4!3, E5, G4!4').out(i)
    again(repeat_stuff, d=0.5, i=i+1)
```
The `!` operator inspired by TidalCycles is used to denote the repetition of a value. You can also sometimes use the `!!` operator from the same family. This operator is a bit special and will be detailed elsewhere.

## Amphibian variables

### Amphibian variables

```python
v.s = 60 # this is an amphibian variable

@swim 
def fun():
    # Calling it and setting it to v.s + 5
    M(note='v.s = v.s + 5').out()
    if random() > 0.8:
        v.s = 60 # resetting so it doesn't go too high
    again(fun)
```
There is a group of variables called *amphibian variables* that are both valid inside and outside the pattern notation. They are defined by `v` followed by a letter from the alphabet (uppercase or lowercase) : `v.a`, `v.A`, `v.Z`, `v.j`. These variables can be freely manipulated from the Python side or from the pattern side. They are totally transparent.

```python
@swim 
def fun(d=0.25):
    # Now having fun with it
    M(note='v.s = v.s + 5|2').out() # more fun
    if random() > 0.8:
        v.s = 50
    again(fun, d=0.25)
```
You can use them to leverage Python or the pattern syntax for what they do best: patterning or dealing with complex algorithmic transformations. Having them both available makes the pattern syntax even more expressive.

There is a finite list of actions you can perform on *amphibian variables*:

- using them (just by calling them)

- setting them (`v.i = 5`)

- resetting them to 0 (`v.i.reset`)

### Amphibian iterators

```python
@swim
def amphi_iter(d=0.25):
    S('amencutup:{1_10}').out(i.i)
    if random() > 0.8:
        i.i = 0
    a(amphi_iter, d=0.25)
```
Similarly to *amphibian variables*, there is a thing called *amphibian iterators* that are valid on both sides. They are defined by `i` followed by a letter from the alphabet (uppercase or lowercase) : `i.a`, `i.A`, `i.Z`, `i.j`. They can be use as substitutes for your regular manual recursive iterators. In the example above, I am using an *amphibian iterator* to summon a breakbeat.

```python
@swim
def amphi_iter(d=0.25):
    S('amencutup:{1_10}', speed='1|2|i.i=0').out(i.i)
    a(amphi_iter, d=0.25)
```
These iterators can be reset or set on the pattern side!

```python
@swim
def amphi_iter(d=0.25):
    if random() > 0.8:
        i.i = [1, 5]
    else:
        i.i = [1, 2]
    S('amencutup:{1_10}', speed='i.v|i.v=[1,2]').out(i.i)
    a(amphi_iter, d=0.25)
```
Similarly, you can define the step value between each value by providing a list of two numbers. This is valid on both sides.
