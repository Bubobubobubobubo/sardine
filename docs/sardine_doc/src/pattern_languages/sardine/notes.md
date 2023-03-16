# Notes

```python
@swim
def notes(p=0.5, i=0):
    D('pluck', midinote='C5 D5 E5 F5 G5', i=i)
    again(notes, p=0.5, i=i+1)
```

Notes are one of the primitives you can use in patterns. Notes will always be converted to some MIDI value (an integer value between `0` and `127`). Notes will be converted to some MIDI value used by **SuperDirt**. If you need more precision, speak in hertzs (`freq=402.230239`).

The syntax to write notes is the following:

1. **[MANDATORY]** capital letter indicating the note name: `C D E F G A B`. **Sardine** also supports the french notation system, so you can write `Do Ré Mi Fa Sol La Si` if it feels more natural to you.
2. **[FACULTATIVE]** flat or sharp: `#`, `b`.
3. **[FACULTATIVE]** octave number: `0..9`.

If you are a robot, you might prefer to speak in numbers. Because notes are turned into numbers, you can everything on them just like if they were numbers. It can be particularly useful to generate custom voicings or weirdly shaped chords that you want to transpose and invert around: `{([0 4 7 9 10 11]+50)^1}`.

# Note qualifiers

```python
@swim
def notes(p=0.5, i=0):
    D('pluck', midinote='C5@penta', i=i)
    again(notes, p=0.5, i=i+1)
```

You can use the `@` operator to **qualify** a note. This will turn a note into a collection of notes based your initial note.
`C@penta` will summon a major pentatonic scale based on the middle C note: `[60 62 64 67 69]`.
Be careful while using them as they will instantly turn a single token into a list of x tokens. You might want to filter part of your newly generated collection or you will just play.. a chord or a scale. You will have to learn techniques to get better at summoning the exact materials you want and some processing by using functions might be needed to get a better result. Writing your patterns by hand is also an option if you are able to think and write down precise harmonic / melodic materials. Check out functions like `(filt)` or `(quant)`.
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


# Chord / Collection inversion

```python
@swim
def notes(p=0.5, i=0):
    D('pluck', midinote='(disco C5@maj7^(0~4))', i=i)
    again(notes, p=0.5, i=i+1)
``` 

You can write chord/sequence inversions using the `^` syntax. It will accept any valid expression like `^(1~5)`. You can also feed negative numbers for inverting a chord downwards. Chord inversions work on anything that is a list. Write custom chords!

# Mathematics on notes

```python
@swim
def notes(p=0.2, i=0):
    D('pluck', midinote='(disco (braid C5 + 10|20|30))', i=i)
    again(notes, p=0.2, i=i+1)
```

You can use arithmetic operators on notes like if they were numbers. Think about it twice. There are many things that are numbers in **Sardine**. It might be fun.

## Polyphony

### Note polyphony

```python
@swim
def poly(p=0.5, i=0):
    D('superpiano', cutoff=500, midinote='{D@maj9} {G@maj7^0} {D@maj9} {G@dim7^1}', i=i, d=2, r=0.25)
    again(poly, p=P('0.5!4 0.25!2', i), i=i+1)
```
    
-   You can use the `{` and `}` delimiters to make parts of your pattern polyphonic.
    - There is **note polyphony**, aka when multiple notes are played together.
    - There is **parametric polyphonic**, aka when the same event is played multiple times with different parameters.
    
There a few rules to understand about polyphony and polyphonic messages. These rules can sound quite counter-intuitive if you think about polyphony just like you think of it on a musical score.
    - The **size** of a polyphonic event &#x2013; meaning the number of messages sent for one occurence of an event &#x2013; is equal to the length of the largest polyphonic pattern you declared.
    
In the first example, we have a 4-5 note polyphony. Every polyphonic element from our pattern is a major 9 or 7 chord (*e.g* `[62, 66, 69, 73, 76]`). It means that if you have a polyphony of `2` somewhere and a polyphony of `4` elsewhere, your first polyphony will be distributed over the second one:
    
    PATTERN:
    
    1.  [1 2 3 4]
    2.  [0 1]
    
    RESULT (POLYPHONY):
    
    1.  [1 2 3 4]
    2.  [0 1 0 1]
    
To illustrate the preceding rule we just talked about, here is a truly bizarre example. Half of our chord is played by a tuned bassdrum, the other half by a piano. Even though this may look odd, this is fully compliant with how parameters are handled by **Sardine**.
    
```python
@swim
def poly(p=0.5, i=0):
    D('{[bd  superpiano]}', cutoff=500, midinote='{D@maj9} {G@maj7^0} {D@maj9} {G@dim7^1}', i=i, d=2, r=0.25)
    again(poly, p=Pat('0.5!4 0.25!2', i), i=i+1)
```   

We have two clear alternations, one between the `superpiano` and `bd` sound sets, the other between the four or five values that form our chords. It is then natural that half of our polyphony will be composed from a tuned bassdrum and the remaining half from a tuned piano. Once you get use to this novel way of thinking about polyphonic patterns, you will see that it opens up some space for interesting polyphonic interactions between sounds :)
It is currently not possible to limit the number of voices generated by an event. Be careful! It is quite easy to get overrun and to kill your computer playing with polyphony!

# Parametric polyphony

```python
@swim
def poly(p=0.5, i=0):
    D('drum:[1 6]', speed='{[1 rand]}  {[2 1.9]}', i=i, d=3)
    D('drum:2', cutoff='{[500:2000 500]*(sin $%rand*80/40)*10}', i=i, d=2)
    D('bd', shape=0.5).out(i, 4)
    again(poly, p=0.5/2, i=i+1)
```   
    
Everything can become polyphonic. Just wrap anything between `{` and `}` and you will return the same event piled up multiple times with different parameters. It allows you to be very creative with patterns.

