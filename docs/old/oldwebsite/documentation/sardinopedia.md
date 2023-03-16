## Demonstration patterns

These patterns are small songs and/or long patterns that you can copy and paste to familiarise yourself with the syntax. Change some values, comment a few lines here and there. Try to learn how to move and alter **Sardine** code.


Play with the `div` amount to generate interesting rhythms.

## Pitch

### Playback speed (S)

```python3
@swim
def hh(d=0.5, i=0):
    S('hh', speed='[1:8]').out(i)
    again(hh, d=0.5, i=i+1)
```
Changing the speed of audio playback for a given audio sample. Cheap version of tuning.

### Sample to pitch (S)

```python3
@swim
def hh(d=0.5, i=0):
    S('hh', midinote='C5!3, E5, G5').out(i)
    again(hh, d=0.5, i=i+1)
```
Pitching an audio sample relatively to a MIDI note.

### Sample to freq (S)

```python3
@swim
def hh(d=0.5, i=0):
    S('hh', freq='100 + (rand*2000)').out(i)
    again(hh, d=0.5, i=i+1)
```
Pitching an audio sample relatively to a given frequency (in `hertz`).


