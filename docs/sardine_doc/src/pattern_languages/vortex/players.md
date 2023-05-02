# Players

## Syntactic Sugar

In accordance with the [TidalCycles](https://tidalcycles.org) model, there are a few players you can use to make your life easier: `d1`, `d2`, `d3`, `d4`, `d5`, `d6`, `d7`, `d8` and `d9`. The players are just thin wrappers and syntactic sugar for the `tidal` function:
```python
d1 = TidalD(name="d1", orbit_number=0)
d2 = TidalD(name="d2", orbit_number=1)
d3 = TidalD(name="d3", orbit_number=2)
d4 = TidalD(name="d4", orbit_number=3)
d5 = TidalD(name="d5", orbit_number=4)
d6 = TidalD(name="d6", orbit_number=5)
d7 = TidalD(name="d7", orbit_number=6)
d8 = TidalD(name="d8", orbit_number=7)
d9 = TidalD(name="d9", orbit_number=8)
```

Each player will be associated with an orbit number. This allows you to add effects to your players without having to think about the orbit you are currently targeting. Please note that the players are also slowed down a bit `.slow(4)` as patterns tend to be quite fast by default.

## The Tidal function

A Tidal pattern can be created using the `tidal` function. The `tidal` function takes two arguments:
- `name`: a name to give to the pattern.
- `pattern`: a pattern or any combination of patterns.

You can use it that way:

```python
tidal('my_pat', s("bd [hh hh:2] sn(2,3) <hh crow>")
                .slow("<4!4 2 0.125>")
                .striate("<2 8>")
                .jux(rev))
```

## Stopping Tidal Patterns

You can stop all the Tidal patterns using the `hush()` function. You can also stop everything by running the base `silence()` or `panic()` functions. You can also stop individual Tidal patterns.

To do so, use the `hush()` function with a *string* or the player that holds the pattern you are willing to stop:

```python
# Using hush on a Tidal Player
d1 * s('bd sn')
hush(d1)

# Using hush with the Tidal function
tidal('dada', s('bd sn'))
hush('dada')
```
