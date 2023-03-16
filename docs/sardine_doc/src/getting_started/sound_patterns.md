# Sound Patterns & Players

The Player is the most basic way to create patterns - it uses a shorthand syntax, and uses patterns and arguments to make musical output.

```python
Pa >> d('bd cp', p=0.5)
```
- `Pa` is a player - it acts on a pattern.
- `d()` is a sender and provides the pattern. It takes any number of arguments.
- `>>` is an operator that assigns the pattern to the player.
- `p=0.5` is an argument where p is shorthand for period.

There are 48 players by default:

```python
# List of all players
all_players = [Pa, Pb, Pc ...Pz, PA, PB, PC, ... PZ]
```

Pattern arguments control the rhythm, pitch and timbre of the pattern. A **Sardine** pattern is **a sandwich of values**. Here is a player with a more detailed pattern:

```python
Pa >> d('bd cp', speed='1 2', shape=0.5, room=0.5, dry=0.25, size=0.1, p='0.5!4  0.25!2')
    
# This is easier to read
Pa >> d('bd cp',
        speed='1 2',
        shape=0.5,
        room=0.5,
        dry=0.25,
        size=0.1,
        period='0.5!4 0.25!2'
)
```

-   `p` or `period`: the rhythm of each step in **beats**. It can be a number (single value) or **string** (pattern).
    -   Period is always relative to the tempo.
    -   Here the period is a string, which makes this a pattern. 0.5 and 0.25 divide the beat, and `0.5!4` means to repeat that step division 4 times.
    -   The note values `bd cp` are applied to the step divisions of the period.
-   `shape`, `room`, etc.: these are parameters of the audio sampler, helping us to shape the sound.

There are two types of arguments you can give to a pattern:

-   **pattern-relative**: these arguments determine how the pattern unfolds in time. These include: `period`, `divisor`, `rate`).
-   **instrument-relative:** these arguments control parameters specific to **SuperDirt** / **MIDI** / **OSC**. For the SuperDirt sampler parameters, refer to the **Audio Engine Reference** in the sidebar.

**Numbers vs Strings:** It is important to know how numbers differ from strings. Numbers are just numbers and can be integers or floats (decimals). Strings are interpreted as **patterns** that are evaluated based on the syntax used. They move in time with each step. In the example above the pattern `"0.5!4, 0.25!2"` when interpreted becomes: `[0.5, 0.5, 0.5, 0.5, 0.25, 0.25]`.

**Summary:**

-   Players (Pa) are used together with an operator (>>) and pattern sender.
-   **Patterns** are a complete description of an algorithmic musical expression: **pitch**, **timbre**, **rhythm**, etc.
-   **Patterns** are a collection of values or other patterns and can take an indefinite amount of arguments.
-   **Patterns** use a special syntax as `'strings'`.

