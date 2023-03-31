# High-level patterns

Once you understand the basic **Sardine** model, you can start thinking about musical patterns at different scales. You can think of patterns in the context of the Sardine pattern language or Ziffers pattern language. You can also think about patterns of these patterns, and so on. In this section, you will learn how to generate musical structures by controlling how your functions are looping, when your functions are looping, etc&#x2026;
There are some functions that apply **globally** to patterns. These functions can be accessed using keyword arguments. They can help you to shape your improvisation, to master repetition and cyclical constructs.

### Span argument (Players only)

The span argument can be used with Players in order to control the flow of time. The `span` argument will compress or extend the duration of your pattern. Think of it as a pattern level event-based time-strecthing method :).

The following patterns are identic. However, note the use of `span`. The first pattern is **1.5** times longer compared to the version without `span`. The second one, on the other hand, is 50% shorter:

```python
Pa >> d('voodoo voodoo:4 linnhats:(rand*20)!4', span=1.5, p=0.5)
Pb >> d('voodoo voodoo:4 linnhats:(rand*20)!4', span=0.5, p=0.5, speed=2)
```

Try to add or remove the `span` argument and listen to the difference.

Play carefully with it as you might sometimes end up with weird rhythmical results, especially if you are already playing complex rhythms with `p`.


## Snap argument (Swimming functions)

`snap` is an additional argument for the `@swim` decorator. `snap` will time-shift the beginning of your pattern around the first beat of the measure:

- `snap=1` will start the pattern one beat after the beginning of the bar.
- `snap=-0.5` will start the pattern half a beat before the beginning of the next bar.

It is a useful function for shifting things around and for synchronising **Sardine** in some scenarios (recording, etc..).


## Until argument

The `until` argument can also be used in the `@swim` decorator for swimming functions and as a regular arguemnt for players. As its name suggests, this argument will loop the function `n` times and stop. This is a very useful trick to use for solos or one-shots events during your sessions:

# It's bouncing ball time!

```python
@swim(until=10)
def baba(p=0.5, i=0):
    D('sid:2',
      legato=0.9,
      speed=0.5,
      lpf='[5000:200,400]',
      i=i
    )
    print(i)
    again(baba, p=P('[1:0.1,0.1]', i), i=i+1)
```

You can also pair it with the `snap` argument if you wish to!

Here is the bouncing ball example from above written using the Players syntax:

```python
Pa >> d('sid:2', until=10, legato=0.9, speed=0.5, lpf=['5000:200,400'], p='[1:0.1,0.1]')
```


## Loaf and On

The `loaf` and `on` arguments can be used in your senders to determine if the pattern should play on a given bar or not. In the following diagram, each `-` represents one bar.:

```python
--------------------------
```

The `loaf` argument will cut slices of time, just like if you were cutting with a knife in a `loaf` of bread:

```python
-------------------------- (time)
---- (loaf=4)
```

Using the `on` argument, you can now select which of these slices your pattern is going to be played on:

```python
-------------------------- (time)
---- (loaf=4)
- -  (on=(1, 3))
```

Note that the `on` argument can be given as an integer or as a integer-based tuple for targetting multiple bars in your `loaf`! In code, the above example would look like:

```python
Pa >> d('bd', loaf=4, on=(1,3))
```

You can create extremely complex rhythmic structures using these two arguments in conjunction with complex patterns!


## On

`on` can also be used alone!


## Euclid and Neuclid

Just like in the Sardine Pattern Language, you can compose euclidian rhythms. This time, these euclidian rhythms will not be composed of single events but of entire bars! This is an extremely funny way to compose complex evolving structures spanning over multiple bars.

```python
Pa >> d('(eu bd 5 8)', p=.5, euclid=(5, 8))
Pb >> d('linnhats', p=.25)
Pc >> d('(eu cp 3 8', p=.5, euclid=(4, 8))
```

`euclid` is the regular euclidian rhythm function while `neuclid` will play the opposite version of that pattern.

## Binary

`binary` is another argument similar to `loaf`, `on`, `euclid` and `neuclid`. Using it, you can declare a boolean structure that will determine if a bar is to be played or not. Use it like so:

```python
Pa >> d('voodoo:[1:10]', binary=[1, 0, 0, 1, 1, 0])
```

This pattern will be played on bars `1`, `4` and `5`. It will cycle every 6 bars and restart :)

## Sometimes

This is a port of the [TidalCycles](https://tidalcycles.org) `sometimes` family of functions:

- `"always"`: 100%
- `"almostAlways"`: 90%
- `"often"`: 75%
- `"sometimes"`: 50%
- `"rarely"`: 25%
- `"AlmostNever"`: 10%
- `"never"`: 0%

These functions represent a likelihood for an event to be played. In order to use these functions, please use the `chance` keyword in any of your patterns:

```python
Pa >> d('linnhats', p=.25, chance="almostAlways")
