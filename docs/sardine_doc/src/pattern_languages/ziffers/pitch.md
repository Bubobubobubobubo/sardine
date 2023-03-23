# Pitch

## Basic syntax

Ziffers is a numbered musical notation and live code golfing language. Melodies are written using numbers `0-9` or characters `'T'` `'E'` 
which can be used in chromatic scale (T=10, E=11).

By default melodies are played in C Major. Examples:

```python
# Play 0 1 2 3 sequentially, in key of C its C D E F:
zplay("0 1 2 3")

# Play 0 and then chord 023:
zplay("0 023")

# Loop the chromatic scale:
ZD('superpiano', '0 1 2 3 4 5 6 7 8 9 T E', scale: :chromatic)

# Loop some notes and chords in D Minor:
ZD('superpiano', "0 023 3 468", key='D', scale='minor')
```

## Scales

Ziffers supports a great number of scales. The list of supported scales is superior to 1000:

```python
...
"Aeradyllian": [1, 1, 1, 1, 1, 1, 1, 2, 2, 1],
"Ryptyllian": [1, 1, 1, 1, 1, 1, 2, 2, 1, 1],
"Loptyllian": [1, 1, 1, 1, 1, 2, 2, 1, 1, 1],
"Kataphyllian": [1, 1, 1, 1, 2, 2, 1, 1, 1, 1],
"Phradyllian": [1, 1, 1, 2, 2, 1, 1, 1, 1, 1],
"Dagyllian": [1, 1, 2, 2, 1, 1, 1, 1, 1, 1],
"Katyllian": [1, 2, 2, 1, 1, 1, 1, 1, 1, 1],
"Gothyllian": [2, 1, 2, 1, 1, 1, 1, 1, 1, 1],
"Lythyllian": [1, 2, 1, 1, 1, 1, 1, 1, 1, 2],
"Bacryllian": [2, 1, 1, 1, 1, 1, 1, 1, 2, 1],
"Aerygyllian": [1, 1, 1, 1, 1, 1, 1, 2, 1, 2],
"Dathyllian": [1, 1, 1, 1, 1, 1, 2, 1, 2, 1],
"Boptyllian": [1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
"Bagyllian": [1, 1, 1, 1, 2, 1, 2, 1, 1, 1],
"Mathyllian": [1, 1, 1, 2, 1, 2, 1, 1, 1, 1],
"Styptyllian": [1, 1, 2, 1, 2, 1, 1, 1, 1, 1],
"Zolyllian": [1, 2, 1, 2, 1, 1, 1, 1, 1, 1],
"Staptyllian": [2, 1, 1, 2, 1, 1, 1, 1, 1, 1],
"Danyllian": [1, 1, 2, 1, 1, 1, 1, 1, 1, 2],
"Goptyllian": [1, 2, 1, 1, 1, 1, 1, 1, 2, 1],
"Epocryllian": [2, 1, 1, 1, 1, 1, 1, 2, 1, 1],
...
```

To get a complete list of scales, [see this file](https://github.com/Bubobubobubobubo/ziffers-python/blob/main/ziffers/defaults.py).

Examples:

```python
Pa * d('superpiano', "q 0 1 2 3") # Defaults to 'major'
Pa * d('superpiano', "q 0 1 2 3", scale= 'minor') # minor scale
Pa * d('superpiano', "q 0 1 2 3", scale='rocitronic') Another one
```

## Note lengths

Default note length is a whole note **q**, which means **1.0** beats of sleep after the note is played. Note lengths can be changed with characters or with decimal notation.

Most common note length are:

- **w** = Whole (Semibreve) = 1.0 = 4.0 beats
- **h** = Half (Minim) = 0.5 = 2.0 beats
- **q** = Quarter (Crotchet) = 0.25 = 1.0 beats
- **e** = Eight (Quaver) = 0.125 = 0.5 beats
- **s** = Sixteenth (Semiquaver) = 0.0625 = 0.25 beats

Note lengths can be defined for all following notes or for single notes by grouping the note length characters. For example note lengths for *Twinkle twinkle little star* could be notated in various ways. Default length is **q** so in this case it is not require to define the length at the start. Note lengths can also be grouped, like **h4**, which means it only affects the given pitch. Alternatively decimals can be used, here in the middle **0.5** is used and then **0.25** is used to change the duration back to quarter note. Alternatively decimal durations can be grouped using **<0.5>1** notation. 

```python
# Twinke twinkle little star
zplay("0 0 4 4 5 5 h4 3 3 2 2 1 1 h0 4 4 3 3 2 2 0.5 1 0.25 4 4 3 3 2 2 <0.5>1 0 0 4 4 5 5 h4 3 3 2 2 1 1 h0")
```