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
}

.md-typeset__table {
    line-height: 2;
}

.md-typeset__table table:not([class]) {
    font-size: .74rem;
    border-right: none;
}

.md-typeset__table table:not([class]) td,
.md-typeset__table table:not([class]) th {
    padding: 9px;
}

/* light mode alternating table bg colors */
.md-typeset__table tr:nth-child(2n) {
    background-color: #f8f8f8;
}

/* dark mode alternating table bg colors */
[data-md-color-scheme="slate"] .md-typeset__table tr:nth-child(2n) {
    background-color: hsla(var(--md-hue),25%,25%,1)
}
</style>

## Sardine Library

**Sardine** is still in an early stage of development. The library is still in an unstable state. The reference will be included after the first stable release. Please refer to the **Sardinopedia** (code examples) or to the **Tutorial** section (long-form article) to learn more about **Sardine** and its usage.

## SuperDirt 


**SuperDirt** documentation is rather scarce and most of it needs to be inferred by looking at the source code. However, the behavior of most parameters is well known -- usually from experience -- by live coders using it. Moreover, **SuperDirt** can be customised freely to add custom effects and synthesizers. I'm working hard on gathering information about each and every parameter I can find :) Some of them are rather arcane. They are probably not meant to be used directly.

Keep in mind that not all of them are useful and that you will likely find better options by building your own environment.

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
|**`size`**         |Size of the reverb                                          |0 -> x        |
|**`dry`**          |Dry/Wet balance                                             |0 -> x        |

##### Delay

The `delay` effect is initially built for Tidal, which is based on a cyclical time representation. However, it has been pre-configured here to work properly with **Sardine**.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`delay`**        |Wet/Dry                                                     |0 -> x        |
|**`delaytime`**    |Delay time                                                  |0 -> x        |
|**`delayfeedback`**|Amount of reinjection of dry signal                         |0 -> x        |

##### Phaser

Not functioning as it should?

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`phaserrate`**   |Speed of phaser (in hz)                                     |0 -> x        |
|**`phaserdepth`**  |Modulation amount                                           |0 -> x        |


##### Leslie

This is a simple emulation of a Leslie rotating speaker typically used in music for treating organ sounds, voices, and to add an eary tint to everything that goes through it. This is basically a way to play creatively with doppler effects.


| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`leslie`**       |Dry/Wet                                                     |0 -> x        |
|**`lrate`**        |Rate                                                        |0 -> x        |
|**`lsize`**       |Wooden cabinet size (in meters)                             |0 -> x        |

```python
@swim 
def test_fx(d=0.25):
    S('jvbass', amp=1, leslie=0.9,
            lrate=0.1, lsize='0.1+r*2').out()
    a(test_fx, d=0.25)
```

#### Filters

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`cutoff`**       |Low-pass filter cutoff frequency (in hertz)                 |0 -> x        |
|**`hcutoff`**      |High-pass filter cutoff frequency (in hertz)                |0 -> x        |
|**`bandf`**        |Bandpass filter cutoff frequency (in hertz)                 |0 -> x        |
|**`resonance`**    |Filter resonance                                            |0 -> 1        |
|**`bandqf`**       |Bandpass resonance                                          |0 -> x        |

#### Distortion

##### Squiz

Will distort your signal, combination of multiple effects put together. It works better if you input multiples of two as parameters.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`squiz`**        |Amount                                                      |0, 2 -> x     |

##### Triode

Very gentle distortion. I actually have no idea about how the `triode` parameter works.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`triode`**       |Distortion amount                                           |0 -> x        |

##### Distort 

Heavy distortion that will/can wildly change the spectrum of your sound.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`distort`**      |Distortion amount                                           |0 -> x        |

##### Shaping 

Shape is an amplifier that can enter distortion territory but with a gentle curve. It will naturally
make your sound louder the more you ramp up the value.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`shape`**        |Amplification amount                                        |0 -> x        |

##### Ring Modulation

Can't make it work on the **Sardine** side.

| Parameter         | Brief description                                          | Typical range|
|-------------------|------------------------------------------------------------|--------------|
|**`ring`**         |Ring modulation amount                                      |0 -> x        |
|**`ringf`**        |Ring modulation frequency                                   |0 -> x        |
|**`ringdf`**       |Modulation frequency slide                                  |0 -> x        |

#### Phasing
#### Shaping

