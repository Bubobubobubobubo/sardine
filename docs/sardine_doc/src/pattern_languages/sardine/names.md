# Names

Names can be used in patterns. They are used for three reasons:
- audio sample and synthesizer names.
- variables in the context of **amphibian variables**
- addresses, a special type of composed name.

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
- Names can't contain any special symbol.

## Sample association

In the context of audio samples, appending a number to a sample using the association operator (`:`) will
complete that name and refer to the `nth` sample in the folder you are designating by the name.

```python
dada:0 # first sound in the dada folder
dada:1 # second sound in the dada folder
```

**Note:** the name can be infinitely high. It does not matter. The number will simply loop around and
only select a valid sample number!

## Synthesizer name and numbers

The same operator (`:`) used on synthesizers can allow you to directly play a note in a pattern:
```python
Pa * d('superpiano:[0 7 0 5]')
```

- These are not MIDI note values but absolute values around C4.
  - Use the `octave` or `oct` parameter to change the base octave.
- Silences are also supported (`.`)

This mechanism can be used as a fast way to write simple looping melodies.
