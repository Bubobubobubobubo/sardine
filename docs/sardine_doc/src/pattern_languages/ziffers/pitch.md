# Pitch

## Basic syntax

Ziffers is a numbered musical notation and live code golfing language. Melodies are written using numbers `0-9` or characters `'T'` `'E'` 
which can be used in chromatic scale (T=10, E=11).

By default melodies are played in C Major. Examples:

```python
# Play 0 1 2 3 sequentially, in key of C its C D E F:
"0 1 2 3"

# Play 0 and then chord 023:
"0 023"

# Play the chromatic scale:
ZD('superpiano', '0 1 2 3 4 5 6 7 8 9 T E', scale: :chromatic)

# Play in D Minor:
D('superpiano', "0 023 3 468", key='D', scale='minor')
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

Default note length is a whole note `w`, which means `4.0` beats of sleep after the note is played. 
Note lengths can be changed with characters, list notation or Z notation.

Most common note length are:

- `w` = Whole (Semibreve)
- `h` = Half (Minim)
- `q` = Quarter (Crotchet)
- `e` = Eight (Quaver)
- `s` = Sixteenth (Semiquaver)

Note lengths can be defined for all following notes or for single notes by grouping the note length
characters. For example note lengths in Blue bird song can be defined using characters `q` (Quarter notes)
for most of the notes and w (Whole notes) by grouping the character with the specific note integer:
```python
"|q 4 2 4 2 |q 4 5 4 2 |q 3 1 3 1 |q 3 4 3 1 |q 4 2 4 2 |q 4 5 4 2 | w4 |q 4 3 2 1 | w0 |"
```


