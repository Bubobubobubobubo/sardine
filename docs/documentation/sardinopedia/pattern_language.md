## Pattern syntax

There is a whole programming language inside of **Sardine**. This language is dedicated to creating patterns of notes, numbers, samples and addresses. It is an ongoing project and might be subject to change in upcoming versions but there is a subset of stable features that you can use without risking your code to break too fast :) The syntax, much like the syntax of a regular general-purpose programming languages is organised in primitive types and things you can do on/with them. It is very reminescent of **Python** but with a twist!

## Primitive types

### Integers and floating-point numbers

```python3
@swim
def number(d=0.5, i=0):
    print(P('1, 1+1, 1*2, 1/3, 1%4, 1+(2+(5/2))', i))
    again(number, d=0.5, i=i+1)
```
You can write numbers (both *integers* and *floating point numbers*) and use common operators such as **addition**, **substraction**, **division**, **multiplication**, **modulo**, etc... For precision in your calculations, you can of course resort to using parentheses. By default, **Sardine** is made so that most arithmetic operators can be used on almost anything, expect if intuitively it doesn't make sense at all like multiplying a string against a string.


#### Time-dependant numbers 

```python3
@swim
def number(d=0.5, i=0):
    print(P('$, r, m, p', i))
    again(number, d=0.5, i=i+1)
```

Some number tokens are clock-time dependant (based on **Sardine** clock time) and refer to a moment in time. Depending on the moment your recursion takes place, you might see some values recurring because you are not polling continuously but polling just a tiny and predictible moment in time. 

- `$`: **tick**, the tick number since the clock started.
- `$.p`: **phase**, a number between `0` and your `c.ppqn`.
- `$.m`: **measure**, the measure since the clock started.


```python3
@swim
def number(d=0.5, i=0):
    print(P('$, $.m, $.p')).out(i)
    again(number, d=0.5, i=i+1)
```

Some other number tokens are absolute-time dependant. They are mostly used for long-running sequences and/or for introducing a random factor in the result of the expression. You will notice that they are prefixed by `$`.

```python3
@swim
def random(d=0.5, i=0):
    print(P('T.U, T.Y, T.M, T.D, T.h, T.m, T.s, T.µ', i))
    again(random, d=0.5, i=i+1)
```

- `T.U`: Unix Time, the current Unix Time.
- `T.Y`: year, the current year.
- `T.M`: month, the current month.
- `T.D`: day, the current day.
- `T.h`: hour, the current hour.
- `T.m`: minute, the current minute.
- `T.s`: second, the current second.
- `T.µ`: microsecond, the current microsecond.

#### Random numbers

You can write random numbers by using the letter `r`. By default, `r` will return a floating point number between `0.0` and `1.0` but it will be casted to integer if it makes more sense in that context (`e.g.` `sample:r*8`).

#### Generating patterns out of time-dependant numbers

```python3
@swim
def random(d=0.5, i=0):
    S('cp', speed='$%20').out(i)
    again(random, d=0.5, i=i+1)
```
Timed tokens make good *low frequency oscillators*, *ramps* or oscillating patterns. Playing with time tokens using modulos, using the `s()`, `c()` or `t()` function is a great way to get generative results out of a predictible sequence. It is very important to practice doing this, especially if you are planning to do some [fast swimming](#advanced-swimming-fast).

### Notes

```python3
@swim
def notes(d=0.5, i=0):
    S('pluck', midinote='C5,D5,E5,F5,G5').out(i)
    again(notes, d=0.5, i=i+1)
```
Notes are one of the primitives you can use in patterns. Notes will always be converted to some MIDI value (an integer value between `0` and `127`). Notes will be converted to some MIDI value used by **SuperDirt**. If you need more precision, speak in hertzs (`freq=402.230239`). Notes are numbers too (!!). You can do math on them if you wish to. The syntax to write notes is the following:

- 1) **[MANDATORY]** capital letter indicating the note name: `C`,`D`,`E`,`F`,`G`,`A`,`B`.
- 2) **[FACULTATIVE]** flat or sharp: `#`, `b`.
- 3) **[FACULTATIVE]** octave number: `0`..`9`.

You can also use french/canadian note names if you will: `Do, Ré, Mi, Fa, Sol, La, Si`. If MIDI is your prefered language and you only think about numbers, use numbers!


#### Note qualifiers

```python3
@swim
def notes(d=0.5, i=0):
    S('pluck', midinote='C5@penta').out(i)
    again(notes, d=0.5, i=i+1)
```
You can use the `@` to **qualify** a note, to summon a collection of notes or a structure based on the provided note. `C@penta` will raise a major pentatonic scale based on middle C. Be careful while using them as they will instantly turn a single token into a list of `x` tokens. You might want to filter part of a qualifiers note collection.

```python

qualifiers = {

    ##########
    # Chords #
    ##########

    "dim": [0, 3, 6, 12],
    "dim9": [0, 3, 6, 9, 14],
    "hdim7": [0, 3, 6, 10],
    "hdim9": [0, 3, 6, 10, 14],
    "hdimb9": [0, 3, 6, 10, 13],
    "dim7": [0, 3, 6, 9],
    "aug": [0, 4, 8, 12],
    "augMaj7": [0, 4, 8, 11],
    "aug7": [0, 4, 8, 10],
    "aug9": [0, 4, 10, 14],
    "maj": [0, 4, 7, 12],
    "maj7": [0, 4, 7, 11],
    "maj9": [0, 4, 11, 14],
    "minmaj7": [0, 3, 7, 11],
    "five": [0, 7, 12],
    "six": [0, 4, 7, 9],
    "seven": [0, 4, 7, 10],
    "nine": [0, 4, 10, 14],
    "b9": [0, 4, 10, 13],
    "mM9": [0, 3, 11, 14],
    "min": [0, 3, 7, 12],
    "min7": [0, 3, 7, 10],
    "min9": [0, 3, 10, 14],
    "sus4": [0, 5, 7, 12],
    "sus2": [0, 2, 7, 12],
    "b5": [0, 4, 6, 12],
    "mb5": [0, 3, 6, 12],

    ##########
    # Scales #
    ##########

    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "hminor": [0, 2, 3, 5, 7, 8, 11],
    "vminor": [0, 2, 3, 5, 7, 8, 10],
    "penta": [0, 2, 4, 7, 9],
    "acoustic": [0, 2, 4, 6, 7, 9, 10],
    "aeolian": [0, 2, 3, 5, 7, 8, 10],
    "algerian": [0, 2, 3, 6, 7, 9, 11, 12, 14, 15, 17],
    "superlocrian": [0, 1, 3, 4, 6, 8, 10],
    "augmented": [0, 3, 4, 7, 8, 11],
    "bebop": [0, 2, 4, 5, 7, 9, 10, 11],
    "blues": [0, 3, 5, 6, 7, 10],
    "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "doubleharmonic": [0, 1, 4, 5, 8, 11],
    "enigmatic": [0, 1, 4, 6, 8, 10, 11],
    "flamenco": [0, 1, 4, 5, 7, 8, 11],
    "gypsy": [0, 2, 3, 6, 7, 8, 10],
    "halfdim": [0, 2, 3, 5, 6, 8, 10],
    "harmmajor": [0, 2, 4, 5, 7, 8, 11],
    "harmminor": [0, 2, 3, 5, 7, 8, 11],
    "hirajoshi": [0, 4, 6, 7, 11],
    "hungarianminor": [0, 2, 3, 6, 7, 8, 11],
    "hungarianmajor": [0, 3, 4, 6, 7, 9, 10],
    "in": [0, 1, 5, 7, 8],
    "insen": [0, 1, 5, 7, 10],
    "ionian": [0, 2, 4, 5, 7, 9, 11],
    "istrian": [0, 1, 3, 4, 6, 7],
    "iwato": [0, 1, 5, 6, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10],
    "lydianaug": [0, 2, 4, 6, 8, 9, 11],
    "lydian": [0, 2, 4, 5, 7, 8, 9, 11],
    "majorlocrian": [0, 2, 4, 5, 6, 8, 10],
    "majorpenta": [0, 2, 4, 7, 9],
    "minorpenta": [0, 3, 5, 7, 10],
    "melominup": [0, 2, 3, 5, 7, 9, 11],
    "melomindown": [0, 2, 3, 5, 7, 8, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "neapolitan": [0, 1, 3, 5, 7, 8, 11],
    "octatonic": [0, 2, 3, 5, 6, 8, 9, 11],
    "octatonic2": [0, 1, 3, 4, 6, 7, 9, 10],
    "persian": [0, 1, 4, 5, 6, 8, 11],
    "phrygian": [0, 1, 4, 5, 7, 8, 10],
    "prometheus": [0, 2, 4, 6, 9, 10],
    "harmonics": [0, 3, 4, 5, 7, 9],
    "tritone": [0, 1, 4, 6, 7, 10],
    "ukrainian": [0, 2, 3, 6, 7, 9, 10],
    "whole": [0, 2, 4, 6, 8, 10],
    "yo": [0, 3, 5, 7, 10],
    "symetrical": [0, 1, 2, 6, 7, 10],
    "symetrical2": [0, 2, 3, 6, 8, 10],
    "messiaen1": [0, 2, 4, 6, 8, 10],
    "messiaen2": [0, 1, 3, 4, 6, 7, 9, 10],
    "messiaen3": [0, 2, 3, 4, 6, 7, 8, 10, 11],
    "messiaen4": [0, 1, 2, 4, 6, 7, 8, 11],
    "messiaen5": [0, 1, 5, 6, 7, 11],
    "messiaen6": [0, 2, 4, 5, 6, 8],
    "messiaen7": [0, 1, 2, 3, 5, 6, 7, 8, 9, 11],

    ##############
    # Structures #
    ##############

    "fourths": [0, 4, 10, 15, 20],
    "fifths": [0, 7, 14, 21, 28],
    "sixths": [0, 9, 17, 26, 35],
    "thirds": [0, 4, 8, 12],
    "octaves": [0, 12, 24, 36, 48],
}
```

These qualifiers are useful in combination with some other functions like `filt()` or `quant()` because they allow you to build complex tonal objets by entering a random list of integers.


#### Note modifiers

```python3
@swim
def notes(d=0.5, i=0):
    S('pluck', midinote='disco(C5@penta)'.out(i)
    again(notes, d=0.5, i=i+1)
```

Functions can be used to further refine the effect of a modifier. There is a long list of functions that you can apply, such as `disco()` or `adisco()` as shown in the preceding example. If you ever wonder about the list of possible functions, refer to the **Sardinopedia** or enter any function name. If the function name is wrong, the list of possible functions will be printed out in the terminal.

#### Chord / Collection inversion


```python3
@swim
def notes(d=0.5, i=0):
    S('pluck', midinote='disco(C5@maj7^4)'.out(i)
    again(notes, d=0.5, i=i+1)
```

You can write chord inversions using the `^` syntax. It will accept any valid expression like `^1~5`. You can also feed negative numbers for inverting a chord downwards. Chord inversions are not only for chords but they also work on lists, which means that you can write custom chords and transpose them up or down :)

#### Mathematics on notes

```python3
@swim
def notes(d=0.5, i=0):
    S('pluck', midinote='disco(braid(C5+0|4|8@penta'))).out(i)
    again(notes, d=0.5, i=i+1)
```
You can use arithmetic operators on notes like if they were a regular number. That's because they are really just numbers! Random and time-dependant numbers are numbers too. Notes are numbers too so you can add a note to a note even if it doesn't really make sense.

### Polyphony

#### Note polyphony

```python
@swim 
def poly(d=0.5, i=0):
    S('<[superpiano]>', cutoff=500, midinote='<D@maj9>, <G@maj7^0>, <D@maj9>, <G@dim7^1>').out(i, 2, 0.25)
    a(poly, d=P('0.5!4, 0.25!2', i), i=i+1)
```
You can use the `<` and `>` delimiters to make parts of your pattern polyphonic. You will soon notice that there are multiple types of polyphony available but the most notable of all, demonstrated in the example above, is the *note polyphony*. It allows you to superpose multiple note events in your patterns just like you expected. However, **Sardine** allows you to deal with polyphony in more unexpected ways. There a few rules to understand about polyphony and polyphonic messages. These rules can sound quite counter-intuitive if you think about it in a traditional way.

The **size** of a polyphonic event -- meaning the number of messages sent for one occurence of an event -- is equal to the length of the largest polyphonic pattern you declared. In the first example, we have a 4-5 note polyphony. Every polyphonic element from our pattern is a major 9 or 7 chord (*e.g* `[62, 66, 69, 73, 76]`). It means that if you have a polyphony of `2` somewhere and a polyphony of `4` elsewhere, your first polyphony will be distributed over the second one:

```
1) [1,2,3,4]
2) [0,1]

RESULT: 
1) [1,2,3,4]
2) [0,1,0,1]
    | | | |
   POLYPHONY 
```
```python
@swim 
def poly(d=0.5, i=0):
    S('<[bd, superpiano]>', cutoff=500, midinote='<D@maj9>, <G@maj7^0>, <D@maj9>, <G@dim7^1>').out(i, 2, 0.25)
    a(poly, d=P('0.5!4, 0.25!2', i), i=i+1)
```
To illustrate the preceding rule we just talked about, here is a truly bizarre example. Half of our chord is played by a tuned bassdrum, the other half by a piano. Even though this may look odd, this is fully compliant with how parameters are handled by **Sardine**. We have two clear alternations, one between the `superpiano` and `bd` sound sets, the other between the four or five values that form our chords. It is then natural that half of our polyphony will be composed from a tuned bassdrum and the remaining half from a tuned piano. Once you get use to this novel way of thinking about polyphonic patterns, you will see that it opens up some space for interesting polyphonic interactions between sounds :)

It is currently not possible to limit the number of voices generated by an event. Be careful! It is quite easy to go from some easy and sparse chords to black MIDI!

#### Parametric polyphony

```python
@swim 
def poly(d=0.5, i=0):
    S('drum:[1,6]', 
            speed='<[1,clamp(r, 0.1, 1)]>, <[2,1.9]>').out(i, 3)
    S('drum:2',
            cutoff='<[500:2000,500]*sin($%r*80/40)*10>').out(i, 2)
    S('bd', shape=0.5).out(i, 4)
    a(poly, d=0.5/2, i=i+1)
```
Everything can become polyphonic. Just wrap anything between `<` and `>` and you will return `x` events, one for each value. It allows you to be very creative with patterns. 

### Names

```python3
@swim
def names(d=0.5, i=0):
    S('bd, pluck, bd, pluck:2+4').out(i)
    again(names, d=0.5, i=i+1)
```
You are using name patterns since you first started to read the **Sardinopedia**! A single letter (if it's not already a note name) can be considered as a name. Be careful! 

#### Addresses

```python3
O(osc_client, "an/address, another/address", value=1, other_value=2).out()
```
Addresses are just like names except that they can contain a `/` separator just like any other typical OSC address out there. They are not really distinct from a name. The difference is only conceptual and in how you use strings.

## Lists and Collections

The **Sardine** pattern notation is built around the idea of having multiple ways to deal with lists and collections. The basic arithmetic syntax and most operators work on single tokens **but will also work on lists**. It means that you can write expressions such as :

```python
[0,1,2,3]%8
[0,2,4,5]*[4,5]
[1:8,0.1]&[2,9]
[0,2,4,5,9,10,12,14]!2
[0,2,4,5,9,10,12,14]!!4
```

There are a few special operators that are only available when you deal with lists.

### Slicing and indexing


```python
@swim 
def test_slice(d=0.5, i=0):
    S('pluck:19', 
            legato=0.2,
            midinote='([60,63,67,69, 71]&[i.i, i.i + 8])^(1~8)').out(i)
    a(test_slice, d=0.125, i=i+1)
```
You can get a slice or just one value from a list by using the special `&` operator. It will work with any list on the right side of the operator but it will only take the first and second value of it no matter what to compose a slice. The index value can be infinite because the index is looping on the list. You can feed a random number generator and get something out. On the down side, it can become quite complex to write very fast, so be careful with it:

```python
@swim 
def test_slice(d=0.5, i=0):
    S('pluck:19', 
            legato=0.2,
            midinote='[60,62, 63,67, 69, 71]^(1~5)&[r, r*4]').out(i)
    a(test_slice, d=0.125, i=i+1)
```

### Extend

```python
@swim 
def test_extend(d=0.5, i=0):
    S('pluck:19', legato=0.2, midinote='[60,62]!2').out(i)
    a(test_extend, d=0.125, i=i+1)
```
Just like with numbers, names and addresses, you can extend a list by calling the `!` operator on it. It will repeat the list `x` times.


### Extend-repeat

```python
@swim 
def test_extend_repeat(d=0.5, i=0):
    S('pluck:19', legato=0.2, midinote='[60,62]!2').out(i)
    a(test_extend_repeat, d=0.125, i=i+1)
```
The variant `!!` now makes sense. It allows you to repeat each individual value in a list `x` times.

## Operations

### Choice 

```python3
@swim
def choosing_stuff(d=0.5, i=0):
    S('bd|pluck', speed='1|2').out(i)
    again(choosing_stuff, d=0.5, i=i+1)
```
The pipe operator `|` can be used on anything to make a 50/50% choice between two tokens. You can also chain them: `1|2|3|4`.

### Ranges

```python3
@swim
def ranges(d=0.5, i=0):
    S('pluck|jvbass', speed='1~5').out(i)
    again(ranges, d=0.5, i=i+1)
```
If you want to generate a number in the range `x` to `y` included, you can use the `~` operator. It spits an integer if you are using integers as boundaries but it will spit out a floating point number if you are using floating point numbers as boundaries. If you use an integer on one side and a floating point number on the other side, a floating point number will be returned.

### Ramps

```python3
@swim
def ramps(d=0.5, i=0):
    S('amencutup:[0:10]', 
        room='[0:1,0.1]',
        cutoff='[1:10]*100').out(i)
    again(ramps, d=0.5, i=i+1)
```
You can generate ramps of integers using the `[1:10]` syntax. This works just like **Python**'s range function. Well, almost... it's way better! You can generate descending ramps easily: `[10:1]`. You can also generate ascending ramps of floating point numbers by precising a step other than `1`: `[1:10,0.5]`. Of course, this also works the other way around :)

### Repeat

```python3
@swim
def repeat_stuff(d=0.5, i=0):
    S('pluck|jvbass', speed='1:2', midinote='C4!4, E4!3, E5, G4!4').out(i)
    again(repeat_stuff, d=0.5, i=i+1)
```
The `!` operator inspired by **TidalCycles** is used to denote the repetition of a value. You can also sometimes use the `!!` operator from the same family. This operator is a bit different, because it is supposed to be used on lists. You can do maths on lists as well with **Sardine**, but this will be detailed in a section later on.

### Silence

```python
@swim 
def silence_demo(d=0.5, i=0):
    S('bd,...').out(i, div=1)
    S('hh,., hh,..').out(i, div=1)
    a(silence_demo, d=1/8, i=i+1)
```

You can use a dot (`.`) inside any pattern to indicate a silence. Silence is a very important and complex topic. Adding silences is a great way to generate interesting patterns. Silences are different for each sender because silence doesn't have the same meaning for a sampler, a MIDI output or an OSC output (`S()`, `M()`, `O()`):

- `S()`: a silence is the absence of a sample. The event will be skipped.

- `M()`: a silence is the absence of a note. The event will be skipped.

- `O()`: a silence is the absence of an address. The event will be skipped.

There is also the interesting case of what I like to call *'parametric silences'*. Take a look at the following example:

```python
@swim 
def silence_demo(d=0.5, i=0):
    S('sitar', legato='0.5', speed='[1:4], .!8').out(i, div=1)
    a(silence_demo, d=1/8, i=i+1)
```

We always have a sample here. There is no **real** silence but we have still have some silences included in the `speed` subpattern. It also has an effect. In the absence of a value for that silence, **Sardine** will backtrack and search the last value that could have been generated by the pattern. The result of the `speed` parameter will then be `[1,2,3,4,8,8,8,8,8,8,8,8]`. For people familiar with modular synthesis, this is pretty much equivalent to a *sample & hold* mechanism.

It is impossible to write a *parametric silence* composed only of silences. It doesn't mean anything to provide a value and actually not providing it.

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
    S('amencutup:[1:10]').out(i.i)
    if random() > 0.8:
        i.i = 0
    a(amphi_iter, d=0.25)
```
Similarly to *amphibian variables*, there is a thing called *amphibian iterators* that are valid on both sides. They are defined by `i` followed by a letter from the alphabet (uppercase or lowercase) : `i.a`, `i.A`, `i.Z`, `i.j`. They can be use as substitutes for your regular manual recursive iterators. In the example above, I am using an *amphibian iterator* to summon a breakbeat.

```python
@swim
def amphi_iter(d=0.25):
    S('amencutup:[1:10]', speed='1|2|i.i=0').out(i.i)
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
    S('amencutup:[1:10]', speed='i.v|i.v=[1,2]').out(i.i)
    a(amphi_iter, d=0.25)
```
Similarly, you can define the step value between each value by providing a list of two numbers. This is valid on both sides.

## The Function Library

**Sardine** pattern notation now comes with a function library. These are functions that should be used directly in the pattern notation to alter a list or a pattern you are working on. They can take basically any input but you will soon figure that some are more specialised than others.

### Sinus, Cosinus, Tangent

* `sin(x)`: **sinus of input** (single tokens or lists). Classic mathematical sinus function.

* `cos(x)`: **cosinus of input** (single tokens or lists). Classic mathematical cosinus function.

* `tan(x)`: **tangent of input** (single tokens or lists). Classic mathematical tangent function.

### Scaling, measuring

* `abs(x)`: Absolute value.
* `max(x)`: Maximum value of list or token itself.
* `min(x)`: Minimum value of list or token itself.
* `mean(x)`: Mean of list or token itself.
* `scale(z, x, y, x', y')`: Bring a value `z` from range `x-y` to range `x'-y'`.
* `clamp(x, y, z)`: Clamp function, limit a value `x` to the minimum `y` to the maximum `z`.

### Reversal, shuffling

* `rev(x)`: Reverse a list.
* `shuf(x)`: Shuffle a list.
* `pal(x)`: palindrome of list.
* `apal(x)`: palindrome of list without repetition of last value.

### Musical functions

* `disco(x)`: Disco function. Every pair note down an octave.
* `adisco(x)`: Anti-disco function. Every pair note up an octave. 
* `bass(x)`: The first note of list is down an octave (not very useful).
* `sopr(x)`: The last note of list is up an octave (not very useful).
* `quant(x, y)`: The last note of list is up an octave (not very useful).

### Voice Leading 

These are two voice leading algorithms. These are only temporary until I figure out a better solution. They usually take a list of four note chords and arrange the voice to minimise movement. They work great but they are not the funniest thing you've ever seen. I'll work on them to make it better!

* `voice(x)`: four-note voice leading algorithm. Naive implementation.
* `dmitri(x)`: four-note voice leading algorithm. Algorithm inspired by Dmitri Tymoczko's work.

### Probabilities 

* `vanish(x, y)`: Takes a list `x`, output only `y`% of values from it.

### Booleans

* `euclid(a, b, c, d)`: Euclidian rhythm function applied to patterns. Takes a pattern `a`, a number of pulses `b`, a number of steps `c` and a rotation amount `d`. Outputs a pattern where the absence of a pulse is a silence and where pulses are values from the pattern.

* `mask(x, y)`: Generalisation of the euclidian rhythm algorithm. Works for any pattern and list of booleans.

### Insertion and rotation

To be documented:

* `in(x, y)`:
* `inp(x, y)`:
* `inrot(x, y)`:
* `inprot(x, y)`:

### Filtering

* `filt(x, y)`:


