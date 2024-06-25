# Names

The **Sardine Pattern Language** is using names for multiple things:
- audio sample and synthesizer names like `kick` or `sawsynth`.
- variable naming in the context of or **internal global variables**.
- addresses, a special type of composed name used for OSC addressing.

```python 
@swim
def names(p=0.5, i=0):
    D('bd pluck bd pluck:(2+4)', i=i)
    again(names, p=0.5, i=i+1)
```

A single letter (if it's not already a note name or a known symbol) can be considered as a name.
Be careful! There are a few hidden rules for names:
- Names can be one letter long but some letters are already taken.
- Names cannot begin with a number.
- Names can't contain any special symbol like `_` or `^`.

## Sample association

In the context of audio samples, appending a number to a sample using the association operator (`:`) will complete that name and refer to the `nth` sample in the folder you are designating by the name. For a synthesizer, the behavior is a little different. It will pitch the synth in semitones.

```python
dada:0 # first sound in the dada folder
dada:1 # second sound in the dada folder
```

**Note:** when indexing on sample names, the number can be infinitely high. It does not matter. The indexing will simply loop around and select a valid sample number!

## Synthesizer name and numbers

The same operator (`:`) used on synthesizers can allow you to directly play a note in a pattern:
```python
Pa * d('superpiano:[0 7 0 5]')
```

- These are not MIDI note values but absolute values around C4.
  - Use the `octave` or `oct` parameter to change the base octave.
- Silences are also supported (`.`)

This mechanism can be used as a fast way to write simple looping melodies.
