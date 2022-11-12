Sampling is taken care of by **SuperDirt** but I don't think that an official documentation of the API exists outside of the documentation provided by libraries using it. So be it, here are some basics for you to get started :)

### Sampler basics

```python3
@swim
def hh(d=0.5):
    S('hh').out(i)
    again(hh, d=0.5)
```
This will play the first file in the `hh` folder, loaded via **SuperDirt**.

```python3
@swim
def hh(d=0.5):
    S('hh:1').out(i)
    again(hh, d=0.5)
```
This will play the second file, etc... Numbers wrap around, so you can't overflow and play a file that doesn't exist. It means that you can iterate freely on the sample number without fear.

### Sample playback speed

```python
@swim
def hh(d=0.5):
    S('jvbass:0', speed='1,2,3,4').out(i.i)
    again(hh, d=0.5)=
```
You can pitch samples up or down by changing the playback speed. `1` is the normal playback speed, `2` twice as fast and `0` will not play anything at all. You can play a file in reverse speed by inputting negative values such as `-1` for backwards normal speed, etc... Beware of very low numbers close to `0` as they will be sometimes harder to hear but will still take memory to be played, especially if there is nothing to stop them.

### Sample playback volume

```python
@swim
def loud(d=0.5):
    S('bd', speed='1', amp=1).out(i.i)
    again(hh, d=0.5)
```
This bassdrum will be played very loud. The `amp` parameter will determine the volume of audio playback for a given sample. `0` equals to silence. `1` corresponds to full volume, with distortion of the audio signal being allowed for larger values.

```python
@swim
def loud(d=0.5):
    S('bd', speed='1', gain=1).out(i.i)
    again(hh, d=0.5)
```
Gain is slightly similar to `amp`. The difference lies in the scaling. While `amp` is defined as a value on a linear scale, `gain` is defined on an exponential scale. The higher you go, the more subtle the change. Folks from the TidalCycles documentation recommend a value between `0` and `1.5` for better use.

### Cutting/Stopping samples

```python
@swim
def cutting(d=0.5):
    S('jvbass:0', legato=0.1).out(i.i)
    again(cutting, d=0.5)
```
The `legato` parameter can be used to cut a sample hard after a given amount of time. It is a very useful parameter not to overlap sounds too much if you ever needed it. It can also be used a safety parameter for playing back long samples without loosing control over the stop time.


```python
@swim
def cutting(d=0.5):
    S('jvbass:0', cut=1).out(i.i)
    again(cutting, d=0.5)
```
The `cut` parameter will cut the previously playing sample if trigerred on the same orbit. This is just like `legato` except that the duration of the `legato` will depend on the time spent between two sounds.


```python
@swim
def cutting(d=0.5):
    S('jvbass:0', sustain=0.01).out(i.i)
    again(cutting, d=0.5)
```
The `sustain` value will determine the length of audio playback (in seconds).

### Sample position

```python
@swim
def position(d=0.5):
    S('fire', speed='1', begin=0.1, end=0.5, amp=0.5).out(i.i)
    again(position, d=2)
```
When playing long audio samples, you might want to *scroll* through the file, moving the playhead accross the file. You can use the `begin` and `end` parameters (from `0` to `1`) to set the begin playback point and the end playback point. You can pattern the `begin` parameter with great expressive effect.

### Sample stretching

```python
@swim
def streeeetch(d=0.5):
    S('fire', 
            begin='r/2',
            legato=1,
            amp=0.5,
            timescale=2.7).out()
    a(streeeetch)
```

You can get some interesting effects by using the `timescale` parameter (between `0` and `3` recommended) for stretching a sample over a given amount of time. This will result in a more *grainy* sound. This is some sort of timestretching for audio samples. Higher values ( >3 ) for timescale work with more distortion to the sound. This can yield interesting results for more experimental sound.
