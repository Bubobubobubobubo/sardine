# Chords

Chords can be played using groups of numbers `"024 357"` or using roman numerals: `i ii iii iv v vi vii`.

```python
"[: i vi v :]" # Play chords as a sequence using default chord length of 1

"q [: iv 1 2 3 iii 2 3 4 ii 4 3 2 i 1 2 3 :]"
```

In major scale (or any other diatonic) roman numerals would correspond to these pitch classes:
```python
i = 024
ii = 135
iii = 246
iv = 357 or 35^0
v = 468 or 46^1
vi = 579 or 5^0^2
vii = 68{10} or 6^1^3
```

Chord key is assigned with the **key** keyword argument (defaults to major). 

## Chord names

Chord names are nice shorthands for similar group of notes. Define chord name using using **^** with 
the name or by using **chord_name** parameter. Chord names work for minor, major and chromatic scales.
Other than that who knows? Not me. Some might work and others might sound a bit funny.

Examples using the chord names:
```python
"i vi^dim"
"i vi"
"i vi^m11+"
"i^7"
"i^maj9" 
```

Chords can also be inverted using % char, for example %1 to invert all following chords up by one:
```python
D('superpiano', 'vii%-2 iii%-1 vi%-1 ii v i%1 iv%2', key='D', scale='minor')
```

List of all chord names (Pitch classes in chromatic scale):

```python
^major  = 047       # ^M
^min  	= 037       # ^minor or ^m
^major7 = 04711     # ^maj7 or ^M7
^7      = 047T      # ^dom7
^m7     = 037{10}   # ^minor7
^aug    = 048       # ^augmented or ^a
^dim    = 036       # ^diminished or ^i
^dim7   = 0369      # ^diminished7 or ^i7
^m7-5   = 036{10}   # ^m7b5 or ^halfdim or ^halfdiminished
^1    	= 0
^5    	= 07
^+5     = 048
^m+5  	= 038
^sus2   = 027
^sus4   = 057
^6    	= 0479
^m6     = 0379
^7sus2	= 027{10}
^7sus4	= 057{10}
^7-5  	= 046{10}
^7+5  	= 048{10}
^m7+5 	= 038{10}
^9    	= 047{10}{14}
^m9     = 037{10}{14}
^m7+9 	= 037{10}{14}
^maj9   = 04711{14}
^9sus4	= 057{10}{14}
^6*9  	= 0479{14}
^m6*9 	= 0379{14}
^7-9  	= 047{10}{13}
^m7-9 	= 037{10}{13}
^7-10 	= 047{10}{15}
^7-11 	= 047{10}{16}
^7-13 	= 047{10}{20}
^9+5  	= 0{10}{13}
^m9+5 	= 0{10}{14}
^7+5-9	= 048{10}{13}
^m7+5-9 = 038{10}{13}
^11   	= 047{10}{14}{17}
^m11    = 037{10}{14}{17}
^maj11  = 04711{14}{17}
^11+  	= 047{10}{14}{18}
^m11+ 	= 037{10}{14}{18}
^13   	= 047{10}{14}{17}{21}
^m13  	= 037{10}{14}{17}{21}
^add2   = 0247
^add4   = 0457
^add9   = 047{14}
^add11  = 047{17}
^add13	= 047{21}
^madd2  = 0237
^madd4  = 0357
^madd9  = 037{14}
^madd11 = 037{17}
^madd13 = 037{21}
```
