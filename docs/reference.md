---
hide:
    - navigation
---
<style>
th, td {
    border: 2px solid var(--md-typeset-table-color);
    border-spacing: 0;
    border-bottom: none;
    border-left: none;
    border-top: none;
    min-width: 100%;
}
.md-typeset__table {
  width: 100%;
}

.md-typeset__table table:not([class]) {
  display: table
}


.md-typeset__table {
    line-height: 2;
    min-width: 100%;
}

.md-typeset__table table:not([class]) {
    font-size: .74rem;
    border-right: none;
}

.md-typeset__table table:not([class]) td,
.md-typeset__table table:not([class]) th {
    padding: 9px;
    min-width: 100%;
}

/* light mode alternating table bg colors */
.md-typeset__table tr:nth-child(2n) {
    background-color: #f8f8f8;
    min-width: 100%;
}

/* dark mode alternating table bg colors */
[data-md-color-scheme="slate"] .md-typeset__table tr:nth-child(2n) {
    background-color: hsla(var(--md-hue),25%,25%,1)
    min-width: 100%;
}
</style>

## SuperDirt 


**SuperDirt** documentation is rather scarce and most of it needs to be inferred by looking at the source code. However, the behavior of most parameters is well known -- usually from experience -- by live coders. Moreover, **SuperDirt** can be customised freely to add custom effects and synthesizers. I'm working hard on gathering information about each and every parameter I can find :) Some of them are rather arcane. They are probably not meant to be used directly. Keep in mind that not all of them are useful and that you will likely find better options by building your own environment.

### Sampling

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`amp`**          |Sound volume (linear scaling)                               |0 -> x        |
|**`gain`**         |Sound volume (exponential scaling)                          |0 -> 1        |
|**`freq`**         |Pitch around given frequency                                |0 -> x        |
|**`midinote`**     |Pitch around given MIDI note                                |0 - 127       |
|**`note`**         |Pitch around given note                                     |???           |
|**`octave`**       |Pitch up or down depending on octave number                 |0 -> x        |
|**`sound`**        |**Implicit** (first argument of `S()`)                      |--------------|
|**`begin`**        |Start position of audio playback                            |0 -> 1        |
|**`end`**          |End position of audio playback                              |0 -> 1        |
|**`accelerate`**   |Rising sample playback speed                                |0 -> x        |
|**`cps`**          |**Implicit** (cycles per second, inherited from Tidal)      |--------------|
|**`loop`**         |???                                                         |???           |
|**`delta`**        |**Unused**                                                  |--------------|
|**`cut`**          |Cut other sounds playing on same orbit, start playing       |0 or 1        |
|**`legato`**       |Play sample for the given duration (without cutting others) |0 -> x        |
|**`pan`**          |Pan sound from left to right speaker (by default)           |0 -> 1        |
|**`orbit`**        |Play sound/synth on the given audio effect bus              |0 -> x        |
|**`latency`**      |Add a latency to audio playback (in seconds)                |0 -> x        |
|**`lag`**          |Similar to latency/offset                                   |0 -> x        |
|**`offset`**       |Similar to latency/lag                                      |0 -> x        |

### Audio effects

#### Space

##### Reverb

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`room`**         |Size of the room                                            |0 -> x        |
|**`size`**         |Size of the reverb - keep below 1 (inf)                     |0 -> 1        |
|**`dry`**          |Dry/Wet balance                                             |0 -> 1        |

```python
@swim 
def test_fx(d=0.25):
    S('hh', amp=1, 
            room='s($.S)', 
            dry=0.1, 
            size='s($)').out()
    a(test_fx, d=0.25)
```

##### Delay

The `delay` effect is initially built for Tidal, which is based on a cyclical time representation. However, it has been pre-configured here to work properly with **Sardine**.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`delay`**        |Wet/Dry                                                     |0 -> 1        |
|**`delaytime`**    |Delay time                                                  |0 -> x        |
|**`delayfeedback`**|Amount of reinjection of dry signal - don't go over 1       |0 -> .99      |


```python
@swim 
def test_fx(d=0.25):
    S('hh', 
            speed='1|2|4',
            delay=1/2, delaytime=1/(2/3),
            delayfeedback='0.5+(r/4)',
            amp=1).out() 
    a(test_fx, d=0.25)
```

##### Phaser

Not functioning as it should?

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`phaserrate`**   |Speed of phaser (in hz)                                     |0 -> x        |
|**`phaserdepth`**  |Modulation amount                                           |0 -> x        |

```python
@swim 
def test_fx(d=0.25):
    S('jvbass', 
            midinote='C|Eb|G|Bb',
            phaserrate='1:10', 
            phaserdepth='s($*2)', amp=1).out() 
    a(test_fx, d=0.5)
```

##### Leslie

This is a simple emulation of a Leslie rotating speaker typically used in music for treating organ sounds, voices, and to add an eary tint to everything that goes through it. This is basically a way to play creatively with doppler effects.


| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`leslie`**       |Dry/Wet                                                     |0 -> x        |
|**`lrate`**        |Rate                                                        |0 -> x        |
|**`lsize`**        |Wooden cabinet size (in meters)                             |0 -> x        |

```python
@swim 
def test_fx(d=0.25):
    S('jvbass', amp=1, leslie=0.9,
            lrate=0.1, lsize='0.1+r*2').out()
    a(test_fx, d=0.25)
```

##### Tremolo

A simple tremolo effect.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`tremolorate`**  |Tremolo speed                                               |0 -> x        |
|**`tremolodepth`** |Depth of tremolo                                            |0 -> x        |


```python
@swim 
def test_fx(d=0.25, i=0):
    S('amencutup:[1:20]', 
            tremolorate='16|32',
            tremolodepth='[0:1,0.25]').out(i)
    a(test_fx, d=0.5, i=i+1)
```

##### Granular weirdness

This is a weird granular effect probably intended to serve as a building block for some other effect but you can use it as is nonetheless. It will slice your audio sample into tiny fragments of it while applying some amount of pitch-shifting on every sample.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`psrate`**       |Pitch-shift rate                                            |0 -> x        |
|**`psdisp`**       |Pitch-shift dispersion                                      |0 -> x        |

```python
@swim 
def test_fx(d=0.25, i=0):
    S('amencutup:[1:20]', 
            psrate='2',
            psdisp='[0:1,0.5]').out(i)
    a(test_fx, d=0.5, i=i+1)
```

#### Filters

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|-------------------|
|**`cutoff`**       |Low-pass filter cutoff frequency (in hertz)                 |0 -> x  us. >2Khz  |
|**`hcutoff`**      |High-pass filter cutoff frequency (in hertz)                |0 -> x  us. < 500hz|
|**`bandf`**        |Bandpass filter cutoff frequency (in hertz)                 |0 -> x             |
|**`resonance`**    |Filter resonance                                            |0 -> 1             |
|**`bandqf`**       |Bandpass resonance                                          |0 -> x             |

```python
@swim 
def test_fx(d=0.25):
    S('jvbass', 
            midinote='C.|C|Eb|G|Bb',
            cutoff='r*7000', resonance='r/2', amp=1).out() 
    a(test_fx, d=0.5)
```

#### Distortion

##### Squiz

Will distort your signal, combination of multiple effects put together. It works better if you input multiples of two as parameters.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`squiz`**        |Amount                                                      |0, 2 -> x     |


```python
@swim 
def test_fx(d=0.25):
    S('tabla:r*200', cut=1, 
            squiz='0|2|4|8',
            midinote='C|F|Bb|E5b', amp=1).out() 
    a(test_fx, d=0.5)
```

##### Triode

Very gentle distortion. I actually have no idea about how the `triode` parameter works.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`triode`**       |Distortion amount                                           |0 -> x        |

```python
@swim 
def test_fx(d=0.25):
    S('tabla:r*200', cut=1, 
            triode='r', # comment me
            midinote='C|F|Bb|E5b', amp=1).out() 
    a(test_fx, d=0.5)
```

##### Distort 

Heavy distortion that will/can wildly change the spectrum of your sound.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`distort`**      |Distortion amount                                           |0 -> x        |

```python
@swim 
def test_fx(d=0.25):
    S('sd:r*200', cut=1, 
            distort='0|0.5',
            midinote='C|G', amp=1).out() 
    a(test_fx, d=0.5)
```

##### Shaping 

Shape is an amplifier that can enter distortion territory but with a gentle curve. It will naturally
make your sound louder the more you ramp up the value.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`shape`**        |Amplification amount                                        |0 -> x        |

```python
@swim 
def test_fx(d=0.25, i=0):
    S('amencutup:[1:20]', shape='[0:1,0.1]').out(i)
    a(test_fx, d=0.5, i=i+1)
```
##### Crush

A very agressive bit crushing effect. Works only when you input multiples of 2. `2` for extreme crushing, `32` for non-discernable.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`crush`**        |Crushing factor                                             |0 -> x        |

```python
@swim 
def test_fx(d=0.25, i=0):
    S('bd, sn, hh, sn', crush=4).out(i)
    a(test_fx, d=0.5, i=i+1)
```

##### Ring Modulation

Can't make it work on the **Sardine** side.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`ring`**         |Ring modulation amount                                      |0 -> x        |
|**`ringf`**        |Ring modulation frequency                                   |0 -> x        |
|**`ringdf`**       |Modulation frequency slide                                  |0 -> x        |

## Sardine Library

**Sardine** is still in an early stage of development. The library is still in an unstable state. The reference will be included after the first stable release. Please refer to the **Sardinopedia** (code examples) or to the **Tutorial** section (long-form article) to learn more about **Sardine** and its usage.
