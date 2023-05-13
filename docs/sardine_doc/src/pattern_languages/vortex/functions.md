# Functions

**Vortex** contains most of the basic **TidalCycles** functions. Here is a comprehensive list of all the functions currently defined in the Python codebase. Take some time to discover them all.

## Concatenative operations

These functions typically take up to **n** patterns to form a single pattern that contains them all, making a sequence.


- `slowcat`: make a single pattern out of multiple patterns without speeding up. The pattern will thus span over multiple cycles.

```python
    d1 * slowcat(
      s('bd*2 sn'), s("jvbass*3"),
      s("drum*2"), s("ht mt")
    )
```

- `fastcat`: make a single pattern out of multiple patterns but mashing all of them into a single cycle. Be careful with long / rich patterns :)

```python
    d1 * fastcat(
      s('bd*2 sn'), s("jvbass*3"),
      s("drum*2"), s("ht mt")
    )
```

- `timecat`: Like `fastcat` except that you provide proportionate sizes of the patterns to each other for when they're concatenated into one cycle. The larger the value in the list, the larger relative size the pattern takes in the final loop. If all values are equal then this is equivalent to `fastcat`.

```python
    d1 * timecat((1, s("bd*4")), (1, s("hh27*8"))))
```

- `randcat`: Pick patterns in a random order. 

```python
    d1 * randcat(
      s('bd*2 sn'), s("jvbass*3"),
      s("drum*2"), s("ht mt")
    )
```


## Superposition and layering


- `jux`: a complex function. It takes your pattern, makes two versions of them, one playing on the left channel, the other on the right channel. It then applies a function but only on the right-hand channel.

```python
    # On the right channel: reversed and filtered
    d1 * s('bd jvbass bd sn').jux(lambda p : p.rev().hpf(500))
```

- `superimpose`: superpose a modified version of a pattern on the top of the original pattern. They are played at the same time, thus superimposed.

```python
    d1 * s('hh cp hh cp').superimpose(lambda p: p.fast(2).rev())
```

- `layer`: Layer up multiple functions on one pattern. For example, the following will play two versions of the pattern at the same time, one reversed and one at twice the speed.

```python
    d1 * s("arpy [~ arpy:4]").layer(rev, lambda p: p.fast(2)])
```

If you want to include the original version of the pattern in the layering, use the `id` function:

```python
    d1 * s("arpy [~ arpy:4]").layer(id, rev, lambda p: p.fast(2)])
```

## Pattern degradation

- `degrade`: randomly removes events from pattern, by 50% chance.

```python
    d1 * s('[bd(5,8), hh(7,8), sn(2,8)]').degrade()
```

- `degrade_by`: Simlar to `degrade` but you can control the percentage of events that are removed with `by`.


```python
    d1 * s('[bd(5,8), hh(7,8), sn(2,8)]').degrade_by(0.2)
```

- `undegrade`: Same as `degrade`, but random values represent percentage of events to keep, not remove, by 50% chance.

```python
    d1 * s('[bd(5,8), hh(7,8), sn(2,8)]').undegrade()
```
- `undegrade_by`: Similar to `degrade` but you can control the percentage of events that are removed with `by`.

```python
    d1 * s('[bd(5,8), hh(7,8), sn(2,8)]').undegrade_by(0.2)
```

## Sometimes family

The `sometimes` family of function can sometimes apply a function to a pattern... but only sometimes :) There is a large family of functions and helper functions to manipulate probabilities.

- `always`: will always apply the function, similar to not using the function and applying directly.

```python
    d1 * s('drum(5,8)').n('1 2 3 4').always(fast(2))
```

- `almostAlways`: will apply the function 90% of the time, at random.

```python
    d1 * s('drum(5,8)').n('1 2 3 4').almostAlways(fast(2))
```

- `often`: will apply the function 75% of the time, at random.

```python
    d1 * s('drum(5,8)').n('1 2 3 4').often(fast(2))
```

- `sometimes`: Applies a function to pattern, around 50% of the time, at random.

```python
    d1 * s('drum(5,8)').n('1 2 3 4').sometimes(fast(2))
```

- `sometimes_by`: Applies a function to pattern sometimes based on specified `by` percentage, at random. `by` is a number between 0 and 1, representing 0% to 100% chance of applying function.

- `sometimes_pre`: Similar to `sometimes` but applies a function to the pattern *before* filtering events 50% of the time, at random.

- `rarely`: will apply the function 25% of the time, at random.

```python
    d1 * s('drum(5,8)').n('1 2 3 4').rarely(fast(2))
```

- `almostNever`: will apply the function 10% of the time, at random.

```python
    d1 * s('drum(5,8)').n('1 2 3 4').almostNever(fast(2))
```

- `never`: will apply the function 0% of the time, at random. The function will thus never be applied.

```python
    d1 * s('drum(5,8)').n('1 2 3 4').never(fast(2))
```

## The every family and friends

- `every`: allows you to apply a function based on a condition. You need a function to determine when the function should be applied (*e.g.* a number **n** to apply the function every **n** cycles). You also need a transformation such as `rev` (reverse a pattern) or `fast` (make a pattern faster).

```python
    d1 * s('[bd(5,8), jvbass(3,8)]').every(3, lambda p: p.superimpose(fast 2))
```

- `somecycles`: ???
- `somecycles_by`: ???

## Operators

- `+` 
- `-`
- `*`
- `/`
- `//`
- `**`
- `>>`
- `<<`

# Pattern speed and timing


- `fast`:
- `slow`
- `early`
- `late`


- `when`
- `when_cycle`
- `off`

- `append`
- `rev`


- `iter`
- `reviter`
- `compress`
- `fastgap`
- `striate`
- `segment`
- `range`
- `rangex`

- `struct`
- `mask`
- `euclid`

- `stack`

## Signals and Generators

Signal functions are functions generating streams of values to apply to a pattern. They are very useful to create low-frequency oscillators or continuously evolving stream of values. These functions should be manipulated to your liking using `segment` and `range`: scaling the stream of generated values, getting the desired granularity/precision of the stream).

### Signal manipulation functions

- `range`: Rescales values to the range `[min, max]`. Assumes pattern is numerical, containing unipolar values in the range `[0, 1]`.
- `segment`: Samples the pattern at a rate of `n` events per cycle. Useful for turning a continuous pattern into a discrete one.

```python
    sine().segment(8).range(4, 8)
```

### Generators

- `sine2`: Bipolar sinusoïdal oscillator: negative and positive values.
- `sine`: Unipolar sinusoïdal oscillator. 
- `cosine2`: Similar to `sine2` but the phase is shifted (*e.g.* cosinus function).
- `cosine`: Similar to `sine` but the phase is shifted (*e.g.* cosinus function).
- `saw2`: Bipolar sawtooth-like oscillator: negative and positive values. 
- `saw`: Unipolar sawtooth-like oscillator.
- `isaw2`: Inverted Bipolar sawtooth-like function.
- `isaw`: Inverted unipolar sawtooth-like function.
- `tri2`: Bipolar triangular oscillator: negative and positive values.
- `tri`: Unipolar triangular oscillator.
- `square2`: Bipolar square wave oscillator: negative and positive values.
- `square`: Unipolar square wave oscillator.
- `rand`: Generate a continuous pattern of pseudo-random numbers between `0` and `1`. 
- `irand`: Generate a pattern of pseudo-random whole numbers between `0` to `n-1` inclusive.

```python
    # generates a pattern of 8 events per cycle
    # with values ranging from 0 to 15 inclusive.
    irand(16).segment(8)
```

- `perlin`: 1D Perlin (smooth) noise, works like `rand` but smoothly moves between random values each cycle.

```python
    perlin().segment(8)
```

## Combinators

- `run`
- `scan`

- `choosewith`
- `choose`
- `choose_cycles`
- `wchoose`
