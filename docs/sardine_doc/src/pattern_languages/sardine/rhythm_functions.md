# Rhythm Functions

This set of functions is all about generating and manipulating rhythms. There are different ways to generate rhythms using Sardine. The system is quite permissive and will allow you to do a lot of things either by manipulating the `period` argument, by filtering some of your events, by adding silences, etc... This variety of approaches is also reflected in the different techniques for applying rhythm generation functions.

# euclid (eu)


This function generates [euclidian rhythms]() by filtering a list of events, replacing some of them by silences. If you take the basic sample `hat` and apply the function by running `(eu hat 5 8)`, you will get the following pattern: `'hat . hat . hat hat . hat'`. As you can see, some events have been removed to generate an euclidian rhythm **on the event side**. There are other algorithms such as **numclid** to generate real temporal euclidian rhythms. This implementation of the euclidian rhythms also supports the typical **rotation** parameter to shift the pattern around.


This function is the bread and butter of many musicians. Spend some time to learn how to use it!

**Arguments:**
- **element:** element to apply the euclidian rhythm (list, sample name, etc.)
- **hits:** how many steps to evenly distribute in the total number of steps.
- **steps:** total number of steps.
- **rotation:** pattern rotation.

**Example:**
```python
Pa * d('(eu kick 5 8)', p=.5)
Pb * d('(eu snare 2 8)', p=.5)
Pc * d('(eu hat 7~8 8)', p=.5)
Pd * d('(eu tom 1~2 8 1)', p=.5)
```

# neuclid (neu)

If euclidian rhythms are a thing, then you can do the opposite and generate the negative of any given euclidian rhythm. This is a super frequent operation that you can do to play on the silent steps of an euclidian rhythm.

**Arguments:**
- **element:** element to apply the euclidian rhythm (list, sample name, etc.)
- **hits:** how many steps to evenly distribute in the total number of steps.
- **steps:** total number of steps.
- **rotation:** pattern rotation.

**Example:**
```python
Pa * d('(eu kick 5 8)', p=.5)
Pb * d('(neu snare 2 8)', p=.5)
Pc * d('(eu hat 7~8 8)', p=.5)
Pd * d('(neu tom 1~2 8 1)', p=.5)
```

# numclid (e)

The algorithms described above (**euclid** and **neuclid**) works by filtering some items in a total number of items. This approach is highly unconventional, even for algorithmic musicians! This new implementation of euclidian rhythms is working differently. It will generate durations that you can use in your `period` argument instead of losing some events. This is what you typically want when you think about euclidian rhythms. The arguments are similar.

**Arguments:**
- **hits:** how many steps to evenly distribute in the total number of steps.
- **steps:** total number of steps.
- **rotation:** pattern rotation.

**Example:**
```python
# We are changing rhythms now!
Pa * d('kick', p='(e 5 8)/2')
Pb * d('snare', p='(e 2 8)/2')
Pc * d('hat', p='(e 7~8 8)/2')
Pd * d('tom', p='(e 1~2 8 1)/2')
```

# binary rhythm (br)

This function is a binary rhythm generator algorithm. Give it any number and this number will be converted to its binary representation. Using this intermediate representation, the number will then be turned into a rhythm using a special algorithm (look at the source if you are interested in the finicky details). You can also rotate the binary number to get more rhythms from the same initial number.

**Arguments:**
- **number:** a number to transform into a binary rhythm.
- **rotation:** rotation applied to the binary intermediate representation.

**Example:**
```python
# Let's take a simple number and generate rhythms from its rotation
Pa * d('kick', p='(br 20 0)/4')
Pb * d('snare', p='(br 20 1)/4')
Pc * d('hat', p='(br 20 2)/[4 2 8!2]!!8')
Pd * d('openhat', p='(br 20 3)/4')
```

## notdot (rest inversion)

```python
Pa * d('(set pk [1 . . .]) * kick')
Pd * d('(notdot (get pk))  * hat')  # outputs [. hat hat hat]
```
