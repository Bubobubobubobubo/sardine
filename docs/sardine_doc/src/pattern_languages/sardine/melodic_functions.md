# Melody Functions

# scl

This function will map any number of numeric arguments to the global melodic scale (defaulting to `major`). You can use the **setscl** function to [set a new global scale](../sardine/variable_functions.md). This is the easiest and fastest way to generate pleasant melodies with Sardine without having to worry about scales/modes, etc.. This is similar to what most beginner friendly music environments are offering to their users.

**Arguments:**
- **...:** list of notes to put on the scale. If the number is higher than the number of notes in the scale, it wraps around and octaves up. Same thing happens if you use negative numbers.
- **octave**: optional octave modifier where `0` returns the scale note without any octaviation, and up.

**Example:**
```python
Pa * d('supersaw', n='C + (scl 0 2 4 0 3 5)', p='(e 5 8 2)/2')
```

# disco

The disco function is a joke. It was initially supposed to mimick the typical disco cliché of playing every note in alternating octave patterns. The name of this function is so easy to remember that it is now used as the *default* function for explaining people how functions work in the **Sardine Pattern Language**.

**Arguments:**
- **...:** notes to disco.
- **depth:** depth for the disco effect. Negative number will jump up octaves. Positive number will jump down octaves.

**Example:**
```python
Pa * d('pluck', n='(disco C Eb G C)', p='.5')
Pa * d('pluck', n='(disco C Eb G C ::depth -2)', p='.5')
```

## quant

Quantize a given list of arguments to the nearest value in the provided set. This set can be any list of numbers or can also be a scale or any other list object that you want to use as a quant reference. The quantized values are clamped in the range of MIDI note values (from `0` to `127`).

**Arguments**:
- **collection:** the collection/list that you want to quantize.
- **reference:** the reference collection/list to quantize to.

**Example:**
```python
(quant [1 2 3 4] maj7) # quantize on a major seventh chord
```

## expand

Chance-based operation. Apply a random octave transposition process to every note in a given collection. There is an optional factor parameter that multiplies the octave transposition.

**Arguments**:
- **collection:**
- **factor:** multiplicator for the expansion amount.

**Example:**
```python
```


