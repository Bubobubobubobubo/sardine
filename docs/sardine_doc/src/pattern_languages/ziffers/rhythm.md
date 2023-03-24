# Rhythm

## Rest or silence

Use `r` to create rhythm with musical rest in the melodies. `r` can be combined with note length, meaning it will sleep the length of the r, for example:

```python
# Play quarter note 1 (D) and then sleep half note and then play half note 2 (E)
zplay("q 0 e3 qr e 2 4 r 1")
```

## Dotted notes

`.` for dotted notes. First dot increases the duration of the basic note by half of its original value. Second dot half of the half, third dot half of the half of the half ... and so on. For example dots added to Whole note `w` will change the duration to 1.5, second dot `w..` to 1.75, third dot to 1.875.

```python
# Row row row your boat using dotted notes
zplay("q. 0 0 | q0 e1 q.2 | q2 e1 q2 e3 | h.4 | e 7 7 7 4 4 4 2 2 2 0 0 0 | q4 e3 q2 e1 | h. 0 ")
```

## Subdivision

Subdivision notation divides the previous note length to equal proportions and can be used to create complex patterns:

```python
# Subdivided from 0.25 by default
zplay("[4 2 4 2] [4 5 4 2] [3 1 3 1] [3 4 3 1] [4 2 4 2] [4 5 4 2] 4 [4 3 2 1] 0")
# Note length for the next subdivision can be defined using characters or decimals
zplay("w [1 2 3 4] 0.5 [1 2 3 4] q [1 2 3 4] w [1 2[3 4]] h [ 1 [ 2 [ 3 [ 4 ]]]]")
```

## Triplets

Triplets can be defined using note characters or by list notation, for example:

```python
# Triplets with note characters
zplay("q 2 6 a 1 3 2 q 5 1 a 4 3 2")

# Triplets with list notation
zplay("q 2 6 h [1 3 2] q 5 1 h [4 3 2]")
```

## Ties

Ties can be created using multiple note length characters. Tied note lengths are summed up for the next degree, for example:

```python
# q+e=0.375
zplay("q 0 qe2 3 4 qe 3 q 4")
```

## List of all note length characters

|	Character	|	Note length	|	Note name (US)	|	Note name (UK)	|	Ticks	|
| - | --- | ------- | ----- | ----- |
|	m	|	8.0	|	Maxima	|	Large	|	15360	|
|	k	|	5.333	|	Triplet long	|	Triplet large	|	10240	|
|	l	|	4.0	|	Long	|	Longa	|	7680	|
|	p	|	2.667	|	Triplet whole	|	Triplet longa	|	5120	|
|	d	|	2.0	|	Double whole note	|	Breve	|	3840	|
|	c	|	1.333	|	Triplet whole	|	Triplet breve	|	2560	|
|	w	|	1.0	|	Whole note	|	Semibreve	|	1920	|
|	y	|	0.667	|	Triplet half	|	Triplet semibreve	|	1280	|
|	h	|	0.5	|	Half note 	|	Minim	|	960	|
|	n	|	0.333	|	Triplet quarter	|	Triplet minim	|	640	|
|	q	|	0.25	|	Quarter note	|	Crotchet	|	480	|
|	a	|	0.167	|	Triplet 8th	|	Triplet crochet 	|	320	|
|	e	|	0.125	|	8th note	|	Quaver	|	240	|
|	f	|	0.083	|	Triplet 16th	|	Triplet quaver	|	160	|
|	s	|	0.0625	|	16th note	|	Semiquaver	|	120	|
|	x	|	0.042	|	Triplet 32th	|	Triplet semiquaver	|	80	|
|	t	|	0.031	|	32th note	|	Demisemiquaver	|	60	|
|	g	|	0.021	|	Triplet 32th	|	Triplet demi-semiquaver	|	40	|
|	u	|	0.016	|	64th note	|	Hemidemisemiquaver	|	30	|
|	j	|	0.0078	|	Triplet 128th	|	Triplet Hemidemisemiquaver	|	15	|
|	o	|	0.00416	|	128th	|	Semihemidemisemiquaver	|	8	|
|	z	|	0.0	|	No length	|	No length	|	0	|


Note that `i`, `v` (chords), `r` (rest) and `b` (flat) are exceptions to a rule that all lower 
letters are note lengths!