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
    S('hh', freq='100 + (r*2000)').out(i)
    again(hh, d=0.5, i=i+1)
```
Pitching an audio sample relatively to a given frequency (in `hertz`).


