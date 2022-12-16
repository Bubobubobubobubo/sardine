## Pitch

### Playback speed (S)

```python3
@swim
def hh(p=0.5, i=0):
    D('hh', speep='[1:8]', i=i)
    again(hh, p=0.5, i=i+1)
```
Changing the speed of audio playback for a given audio sample. Cheap version of tuning.

### Sample to pitch (S)

```python3
@swim
def hh(p=0.5, i=0):
    D('hh', midinote='C5!3, E5, G5', i=i)
    again(hh, p=0.5, i=i+1)
```
Pitching an audio sample relatively to a MIDI note.

### Sample to freq (S)

```python3
@swim
def hh(p=0.5, i=0):
    D('hh', freq='100 + (r*2000)', i=i)
    again(hh, p=0.5, i=i+1)
```
Pitching an audio sample relatively to a given frequency (in `hertz`).
