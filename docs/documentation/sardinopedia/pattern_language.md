## I - The Sardine Pattern Language

I have talked a fair bit about the **internal programming language** used by **Sardine**. Let's deep dive and learn more about it. This language is dedicated to creating patterns of notes, numbers, samples and addresses. It is an ongoing project and might be subject to change in upcoming versions but there is a subset of stable features that you can use without risking your code to break too fast :) The syntax, much like the syntax of a regular general-purpose programming languages is organised in primitive types and unary / binary operators or functions you can apply on/to them. It is very reminescent of **Python** but with a twist!

I am not very skilled at developing custom programming languages but the plan.. you get it.. is to get better at it by practising and getting help from others. If you already know how to build things like this, the architecture for the **Sardine** language is rather sane and self-contained. The language can be developed and tested against unit tests. Go for it!

## II - Primitive types

### A) Integers and floating-point numbers

```python3
@swim
def number(p=0.5, i=0):
    print(Pat('1, 1+1, 1*2, 1/3, 1%4, 1+(2+(5/2))', i))
    again(number, p=0.5, i=i+1)
```

You can write numbers (both *integers* and *floating point numbers*) and use common operators such as **addition**, **substraction**, **division**, **multiplication**, **modulo**, etc... For precision in your calculations, you can of course resort to using parentheses. By default, **Sardine** is made so that most arithmetic operators can be used on almost anything, expect if intuitively it doesn't make sense at all like multiplying a string against a string.

**Let's stop for a moment and try to remember the following**: you can apply arithmetics to numbers but also to lists! You can for instance write an addition between a number and a list, between two lists, between a number and a note, between a chord and a list, etc.. All of this is supported by the language. Incidentally, it means that functions that work on lists can also work on single tokens. It also means that functions that are supposed to work for single numbers will work for lists, because the function will be mapped to every element in the list. It turns the act of composing patterns into a rather organic process.

#### a1) Time-dependant numbers

```python3
@swim
def number(p=0.5, i=0):
    print(Pat('$, r, m, p', i))
    again(number, p=0.5, i=i+1)
```

Some number tokens are clock-time dependant (based on **Sardine** clock time) and refer to a moment in time. Depending on the moment your recursion takes place, you might see some values recurring because you are not polling continuously but polling just a tiny and predictible moment in time.

- `$`: **tick**, the tick number since the clock started.
- `$.p`: **phase**, a number between `0` and your `c.ppqn`.
- `$.m`: **measure**, the measure since the clock started.


```python3
@swim
def number(p=0.5, i=0):
    print(Pat('$, $.m, $.p', i))
    again(number, p=0.5, i=i+1)
```

Some other number tokens are absolute-time dependant. They are mostly used for long-running sequences and/or for introducing a random factor in the result of the expression. You will notice that they are prefixed by `$`.

```python3
@swim
def rand(p=0.5, i=0):
    print(Pat('T.U, T.Y, T.M, T.D, T.h, T.m, T.s, T.µ', i))
    again(rand, p=0.5, i=i+1)
```

- `T.U`: Unix Time, the current Unix Time.
- `T.Y`: year, the current year.
- `T.M`: month, the current month.
- `T.D`: day, the current day.
- `T.h`: hour, the current hour.
- `T.m`: minute, the current minute.
- `T.s`: second, the current second.
- `T.µ`: microsecond, the current microsecond.

#### a2) Random numbers

You can write random numbers by using the letter `r`. By default, `r` will return a floating point number between `0.0` and `1.0` but it will be casted to integer if it makes more sense in that context (`e.g.` `sample:r*8`). This is not the only way to generate a random number. For instance, `r` and `0.0~1.0` yield a similar result. Redundancy is good when working with a programming language!

#### a3) Patterns out of time

```python3
@swim
def outof(p=0.5, i=0):
    D('cp', speed='$%20', i=i)
    again(outof, p=0.5, i=i+1)
```

Timed tokens make good *low frequency oscillators*, *ramps* or oscillating patterns. Playing with time tokens using modulos or the `sin()`, `coD()` or `tan()` functions is a great way to get generative results out of a predictible sequence. It is very important to practice doing this, especially if you are planning to use *fast swimming functions*. The faster you recurse, the better your timing resolution. You can start to enter into the realm of signal-like patterns that can be particularly good for generating fluid patterns.

### B) Notes

```python3
@swim
def note(p=0.5, i=0):
    D('pluck', midinote='C5,D5,E5,F5,G5', i=i)
    again(notes, p=0.5, i=i+1)
```

Notes are one of the primitives you can use in patterns. Notes will always be converted to some MIDI value (an integer value between `0` and `127`). Notes will be converted to some MIDI value used by **SuperDirt**. If you need more precision, speak in hertzs (`freq=402.230239`). Notes are numbers too (!!). You can do math on them if you wish to. The syntax to write notes is the following:

- 1) **[MANDATORY]** capital letter indicating the note name: `C`,`D`,`E`,`F`,`G`,`A`,`B`. **Sardine** also supports the french notation system, so you can write `Do, Ré, Mi, Fa, Sol, La, Si` if it feels more natural to you :)
- 2) **[FACULTATIVE]** flat or sharp: `#`, `b`.
- 3) **[FACULTATIVE]** octave number: `0`..`9`.

Of course, if you are a robot, you might prefer to speak in numbers. Because notes are turned into numbers, you can do this and **Sardine** will not complain. It can be particularly useful to generate custom voicings or weirdly shaped chords that you want to transpose and invert around: `<([0,4,7,9,10,11]+50)^1>`.


#### b1) Note qualifiers

```python3
@swim
def note(p=0.5, i=0):
    D('pluck', midinote='C5@penta', i=i)
    again(notes, p=0.5, i=i+1)
```

You can use the `@` operator to **qualify** a note (or a number?). This will turn a note into  a collection of notes / structure based on the targetted note. `C@penta` will summon a major pentatonic scale based on the middle C note: `[60, 62, 64, 67, 69]`. Be careful while using them as they will instantly turn a single token into a list of `x` tokens. You might want to filter part of a qualifiers note collection.

You will soon find out that it can be cumbersome to summon a long list of notes from the realm of oblivion. You will have to learn techniques to get better at summoning the exact materials you want and some processing by using functions might be needed to get a better result. Writing your patterns by hand is also an option if you are able to think and write down precise harmonic / melodic materials. Check out functions like `filt()` or `quant()`.

Take note that the following list is not always perfectly up to date. Moreover, it can be particularly tricky for you to remember how I named some of the structures:

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

#### b2) Note modifiers

```python3
@swim
def note(p=0.5, i=0):
    D('pluck', midinote='disco(C5@penta)', i=i)
    again(notes, p=0.5, i=i+1)
```

Functions can be used to further refine the effect of a modifier. There is a long list of functions that you can apply, such as `disco()` or `adisco()` as shown in the preceding example. If you ever wonder about the list of possible functions, refer to the **Sardinopedia** or enter any function name. If the function name is wrong, the list of possible functions will be printed out in the terminal.

#### b3) Chord / Collection inversion


```python3
@swim
def note(p=0.5, i=0):
    D('pluck', midinote='disco(C5@maj7^4)', i=i)
    again(notes, p=0.5, i=i+1)
```

You can write chord inversions using the `^` syntax. It will accept any valid expression like `^1~5`. You can also feed negative numbers for inverting a chord downwards. Chord inversions are not only for chords but they also work on lists, which means that you can write custom chords and transpose them up or down :)

#### b4) Mathematics on notes

```python3
@swim
def note(p=0.5, i=0):
    D('pluck', midinote='disco(braid(C5+0|4|8@penta')), i=i)
    again(notes, p=0.5, i=i+1)
```
You can use arithmetic operators on notes like if they were a regular number. That's because they are really just numbers! Random and time-dependant numbers are numbers too. Notes are numbers too so you can add a note to a note even if it doesn't really make sense. It will also not probably sound very good because notes are clamped in the range from `0` to `127`.

#### b5) Polyphony

##### Note polyphony

```python
@swim
def poly(p=0.5, i=0):
    D('<[superpiano]>', cutoff=500, midinote='<D@maj9>, <G@maj7^0>, <D@maj9>, <G@dim7^1>', i=i, d=2, r=0.25)
    again(poly, p=Pat('0.5!4, 0.25!2', i), i=i+1)
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
def poly(p=0.5, i=0):
    D('<[bd, superpiano]>', cutoff=500, midinote='<D@maj9>, <G@maj7^0>, <D@maj9>, <G@dim7^1>', i=i, d=2, r=0.25)
    again(poly, p=Pat('0.5!4, 0.25!2', i), i=i+1)
```

To illustrate the preceding rule we just talked about, here is a truly bizarre example. Half of our chord is played by a tuned bassdrum, the other half by a piano. Even though this may look odd, this is fully compliant with how parameters are handled by **Sardine**. We have two clear alternations, one between the `superpiano` and `bd` sound sets, the other between the four or five values that form our chords. It is then natural that half of our polyphony will be composed from a tuned bassdrum and the remaining half from a tuned piano. Once you get use to this novel way of thinking about polyphonic patterns, you will see that it opens up some space for interesting polyphonic interactions between sounds :)

It is currently not possible to limit the number of voices generated by an event. Be careful! It is quite easy to go from some easy and sparse chords to black MIDI!

##### Parametric polyphony

```python
@swim
def poly(p=0.5, i=0):
    D('drum:[1,6]', speed='<[1,clamPat(r, 0.1, 1)]>, <[2,1.9]>', i=i, d=3)
    D('drum:2', cutoff='<[500:2000,500]*sin($%rand*80/40)*10>', i=i, d=2)
    D('bd', shape=0.5).out(i, 4)
    again(poly, p=0.5/2, i=i+1)
```
Everything can become polyphonic. Just wrap anything between `<` and `>` and you will return `x` events, one for each value. It allows you to be very creative with patterns.

### C) Names

```python3
@swim
def name(p=0.5, i=0):
    D('bd, pluck, bd, pluck:2+4', i=i)
    again(names, p=0.5, i=i+1)
```

You are using name patterns since you first started to read the **Sardinopedia**! A single letter (if it's not already a note name) can be considered as a name. Be careful! There are a few hidden rules for names. Names can be one letter long but some letters are already taken by some parts of the language (such as `r`). Names cannot begin with a number. It is also forbidden to use any symbol inside your names.

### D) Addresses

```python3
O(osc_client, "an/address, another/address", value=1, other_value=2)
```

Addresses are just like names except that they can contain a `/` separator just like any other typical OSC address out there. They are not really distinct from a name. The difference is only conceptual and in the usage of your strings.

## II - Lists and Collections

The **Sardine** pattern notation is built around the idea of having multiple ways to deal with linear lists and collections. The basic arithmetic syntax and most operators work on single tokens **but will also work on lists**. It means that you can write expressions such as :

```python
[0,1,2,3]%8
[0,2,4,5]*[4,5]
[1:8,0.1]&[2,9]
[0,2,4,5,9,10,12,14]!2
[0,2,4,5,9,10,12,14]!!4
```

There are a few special operators that are only available when you deal with lists. This is something you will get familiar with by trying. You will see that most things work while some will not yield the result you expect.

### A) Slicing and indexing

```python
@swim
def test_slice(p=0.5, i=0):
    D('pluck:19',
            legato=0.2,
            midinote='([60,63,67,69, 71]&[i.i, i.i + 8])^(1~8)', i=i)
    again(test_slice, p=0.125, i=i+1)
```

You can get a slice or just one value from a list by using the special `&` operator. It will work with any list on the right side of the operator but it will only take the first and second value of it no matter what to compose a slice. The index value can be infinite because the index is looping on the list. You can feed a random number generator and get something out. On the down side, it can become quite complex to write very fast, so be careful with it:

```python
@swim
def test_slice(p=0.5, i=0):
    D('pluck:19',
            legato=0.2,
            midinote='[60,62, 63,67, 69, 71]^(1~5)&[r, rand*4]', i=i)
    again(test_slice, p=0.125, i=i+1)
```

### B) Extend

```python
@swim
def test_extend(p=0.5, i=0):
    D('pluck:19', legato=0.2, midinote='[60,62]!2', i=i)
    again(test_extend, p=0.125, i=i+1)
```

Just like with numbers, names and addresses, you can extend a list by calling the `!` operator on it. It will repeat the list `x` times.

### C) Extend-repeat

```python
@swim
def test_extend_repeat(p=0.5, i=0):
    D('pluck:19', legato=0.2, midinote='[60,62,63]!!3', i=i) #note the repetition of values within the list
    again(test_extend_repeat, p=0.125, i=i+1)
```
The variant `!!` now makes sense. It allows you to repeat each individual value in a list `x` times.

## III - Operators

### A) Choice 

```python3
@swim
def choosing_stuff(p=0.5, i=0):
    D('bd|pluck', speed='1|2', i=i)
    again(choosing_stuff, p=0.5, i=i+1)
```
The pipe operator `|` can be used on anything to make a 50/50% choice between two tokens. You can also chain them: `1|2|3|4`. The behavior of chaining multiple choice operators has not been clearly defined. The distribution might not be the one you expect.

### B) Ranges

```python3
@swim
def rangeD(p=0.5, i=0):
    D('pluck|jvbass', speed='1~5', i=i)
    again(ranges, p=0.5, i=i+1)
```

If you want to generate a number in the range `x` to `y` included, you can use the `~` operator. It spits an integer if you are using integers as boundaries but it will spit out a floating point number if you are using floating point numbers as boundaries. If you use an integer on one side and a floating point number on the other side, a floating point number will be returned. It can be used as an alternative to the `r` token for generating random numbers.

### C) Ramps

```python3
@swim
def rampD(p=0.5, i=0):
    D('amencutup:[0:10]',
        room='[0:1,0.1]',
        cutoff='[1:10]*100', i=i)
    again(ramps, p=0.5, i=i+1)
```

You can generate ramps of integers using the `[1:10]` syntax. This works just like **Python**'s range function. Well, almost... it's way better! You can generate descending ramps easily: `[10:1]`. You can also generate ascending ramps of floating point numbers by precising a step other than `1`: `[1:10,0.5]`. Of course, this also works the other way around :)

### D) Repeat

```python3
@swim
def repeat_stuff(p=0.5, i=0):
    D('pluck|jvbass', speed='1:2', midinote='C4!4, E4!3, E5, G4!4', i=i)
    again(repeat_stuff, p=0.5, i=i+1)
```

The `!` operator inspired by **TidalCycles** is used to denote the repetition of a value. You can also sometimes use the `!!` operator from the same family. This operator is a bit different, because it is supposed to be used on lists. You can do maths on lists as well with **Sardine**, but this will be detailed in a section later on.

### E) Silence

```python
@swim
def silence_demo(p=0.5, i=0):
    D('bd,...', i=i, d=1)
    D('hh,., hh,..', i=i, d=1)
    again(silence_demo, p=1/8, i=i+1)
```

You can use a dot (`.`) inside any pattern to indicate a silence. Silence is a very important and complex topic. Adding silences is a great way to generate interesting patterns. Silences are different for each sender because silence doesn't have the same meaning for a sampler, a MIDI output or an OSC output (`D()`, `N()`, `O()`):

- `D()`: a silence is the absence of a sample. The event will be skipped.

- `N()`: a silence is the absence of a note. The event will be skipped.

- `O()` (any OSC based Sender): a silence is the absence of an address. The event will be skipped.

There is also the interesting case of what I like to call *'parametric silences'*. Take a look at the following example:

```python
@swim
def silence_demo(p=0.5, i=0):
    D('sitar', legato='0.5', speed='[1:4], .!8', i=i, d=1)
    again(silence_demo, p=1/8, i=i+1)
```

We always have a sample here. There is no **real** silence but we have still have some silences included in the `speed` subpattern. It also has an effect. In the absence of a value for that silence, **Sardine** will backtrack and search the last value that could have been generated by the pattern. The result of the `speed` parameter will then be `[1,2,3,4,8,8,8,8,8,8,8,8]`. For people familiar with modular synthesis, this is pretty much equivalent to a *sample & hold* mechanism.

It is impossible to write a *parametric silence* composed only of silences. It doesn't mean anything to provide a value and actually not providing it.

## IV - Amphibian variables

### A) Amphibian variables

```python
V.s = 60 # this is an amphibian variable

@swim
def fun():
    # Calling it and setting it to v.s + 5
    N(note='v.s = v.s + 5')
    if random() > 0.8:
        V.s = 60 # resetting so it doesn't go too high
    again(fun)
```

There is a group of variables called *amphibian variables* that are both valid inside and outside the pattern notation. They are defined by `v` followed by a letter from the alphabet (uppercase or lowercase) : `V.a`, `V.A`, `V.Z`, `V.j`. These variables can be freely manipulated from the Python side or from the pattern side. They are totally transparent.

```python
@swim
def fun(p=0.25):
    # Now having fun with it
    N(note='v.s = v.s + 5|2') # more fun
    if random() > 0.8:
        v.s = 50
    again(fun, p=0.25)
```

You can use them to leverage Python or the pattern syntax for what they do best: patterning or dealing with complex algorithmic transformations. Having them both available makes the pattern syntax even more expressive.

There is a finite list of actions you can perform on *amphibian variables*:

- using them (just by calling them)

- setting them (`V.i = 5`)

- resetting them to 0 (`V.i.reset`)

### B) Amphibian iterators

```python
@swim
def amphi_iter(p=0.25):
    D('amencutup:[1:10]', i=i.i)
    if random() > 0.8:
        i.i = 0
    again(amphi_iter, p=0.25)
```

Similarly to *amphibian variables*, there is a thing called *amphibian iterators* that are valid on both sides. They are defined by `I` followed by a letter from the alphabet (uppercase or lowercase) : `I.a`, `I.A`, `I.Z`, `I.j`. They can be use as substitutes for your regular manual recursive iterators. In the example above, I am using an *amphibian iterator* to summon a breakbeat.

```python
@swim
def amphi_iter(p=0.25):
    D('amencutup:[1:10]', speed='1|2|i.i=0', i=i.i)
    again(amphi_iter, p=0.25)
```

These iterators can be reset or set on the pattern side!

```python
@swim
def amphi_iter(p=0.25):
    if random() > 0.8:
        I.i = [1, 5]
    else:
        i.i = [1, 2]
    D('amencutup:[1:10]', speed='i.v|i.v=[1,2]', i=i.i)
    again(amphi_iter, p=0.25)
```
Similarly, you can define the step value between each value by providing a list of two numbers. This is valid on both sides.

## V - The Function Library

**Sardine** pattern notation now comes with a function library. These are functions that should be used directly in the pattern notation to alter a list or a pattern you are working on. They can take basically any input but you will soon figure that some are more specialised than others. This is the part of the language that is the more subject to changes in upcoming versions. That's why I am only talking about it now, at the bottom of a fairly long page.

I want to explore how far you can go by introducing functional concepts to handle linear sequences. So far, only functions are available. The next step will be to introduce high-order functions and to build a small set of functional operations to pattern functions themselves. Only then will I be happy. I will base myself on that work to write a decent and complex function library.


### A) Sinus, Cosinus, Tangent

* `sin(x)`: **sinus of input** (single tokens or lists). Classic mathematical sinus function.

* `cos(x)`: **cosinus of input** (single tokens or lists). Classic mathematical cosinus function.

* `tan(x)`: **tangent of input** (single tokens or lists). Classic mathematical tangent function.

### B) Scaling, measuring

* `abs(x)`: Absolute value.
* `max(x)`: Maximum value of list or token itself.
* `min(x)`: Minimum value of list or token itself.
* `mean(x)`: Mean of list or token itself.
* `scale(z, x, y, x', y')`: Bring a value `z` from range `x-y` to range `x'-y'`.
* `clamPat(x, y, z)`: Clamp function, limit a value `x` to the minimum `y` to the maximum `z`.

### C) Reversal, shuffling

* `rev(x)`: Reverse a list.
* `shuf(x)`: Shuffle a list.
* `pal(x)`: palindrome of list.
* `apal(x)`: palindrome of list without repetition of last value.

### D) Musical functions

* `disco(x)`: Disco function. Every pair note down an octave.
* `adisco(x)`: Anti-disco function. Every pair note up an octave.
* `bass(x)`: The first note of list is down an octave (not very useful).
* `sopr(x)`: The last note of list is up an octave (not very useful).
* `quant(x, y)`: The last note of list is up an octave (not very useful).

### E) Voice Leading

These are two voice leading algorithms. These are only temporary until I figure out a better solution. They usually take a list of four note chords and arrange the voice to minimise movement. They work great but they are not the funniest thing you've ever seen. I'll work on them to make it better!

* `voice(x)`: four-note voice leading algorithm. Naive implementation.
* `dmitri(x)`: four-note voice leading algorithm. Algorithm inspired by Dmitri Tymoczko's work.

### F) Probabilities 

* `vanish(x, y)`: Takes a list `x`, output only `y`% of values from it.

### G) Booleans

* `euclid(a, b, c, d)`: Euclidian rhythm function applied to patterns. Takes a pattern `a`, a number of pulses `b`, a number of steps `c` and a rotation amount `d`. Outputs a pattern where the absence of a pulse is a silence and where pulses are values from the pattern.

* `mask(x, y)`: Generalisation of the euclidian rhythm algorithm. Works for any pattern and list of booleans.

### H) Insertion and rotation

To be documented:

* `in(x, y)`:
* `inPat(x, y)`:
* `inrot(x, y)`:
* `inprot(x, y)`:

### I) Filtering

* `filt(x, y)`:
