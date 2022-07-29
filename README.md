# Sardine

Sardine is a small fun summer project made using asyncio and the [mido MIDI Library](https://github.com/mido/mido). It is an attempt to get a small MIDI Clock and MIDI scheduling library ready for sequencing synthesizers and hardware drum machines on-the-fly. For the time being, I will try to support the whole range of MIDI messages before trying to branch out using OSC.

## Installation

Installation is pretty simple:
1) run `setup.py` using `pip3 install -e .` to download required libraries and install the library.
2) open a new interactive session using `python3 -m asyncio`
   - **/!\\ Make sure that you are running the asyncio REPL!**
3) import the library `from sardine import *`
4) Follow the prompt to connect to a MIDI Output.

## Debug

If you encounter a bug at startup, feel free to tweak the `__init__.py` file of the library. I am developing `Sardine` for my own usage right now. Some configuration variables might still refer to my own local environment...

## Usage

### The internal Clock

As soon as the library is imported, an instance of `Clock` will start to run in the background and will be referenced to by the variable `c` (in lowercase). `Clock` is the main MIDI Clock you will be playing with. Because the project is still very experimental and things move often, you won't have to worry a lot about the internals. Just remember that some methods could be useful:
* `c.bpm`: current BPM (can be inexact depending on your `ppqn`)
* `c.ppqn`: current [PPQN](https://en.wikipedia.org/wiki/Pulses_per_quarter_note) (1-??).
  - be careful. The tempo might fluctuate based on the PPQN you choose.
* `c.get_tick_duration`: duration of a clock tick.

`c.bpm` and `c.ppqn` can be manually adjusted if you feel like it. Be careful, changing these values can result in a dramatic tempo shift. I still need to work a little bit on the internals to make this correct :).

For now, the clock is limited to MIDI output only. It means that you can open a DAW such as Ableton or Bitwig and use `Sardine` as your MIDI Clock. MIDI Clock In is a feature I still need to code in :) and is not yet supported.

There are some sugared functions to schedule coroutines on the clock:
- `cs` (`c.schedule(coro)`): introduce a new coroutine.
- `cr` (`c.remove(coro)`): remove a coroutine.

More functions will be added to take care of scheduling on the clock.

### Temporal recursive functions

For an introduction about temporal recursion, please read this [short paper](http://extempore.moso.com.au/temporal_recursion.html) written by Andrew Sorensen. Even though the examples are written in Scheme, I am following a very similar design for `Sardine`. Asynchronous functions can be scheduled to run periodically on the clock and support temporal recursion! It means that you can write the following and expect the following output:

```python
# A basic temporal recursive function
async def incr(delay=20, num=0):
    num += 1
    print(f"Num: {num}")
    loop(num(delay=20, num))

# Scheduling it on the clock
cs(num(delay=20, num=0))

# Output
# Num: 1
# Num: 2
# Num: 3
# Num: 4
# Num: 5
```

This is an incredibely useful feature to keep track of state between iterations of your function. It has some musical implications as well! Temporal recursion makes it very easy to manually code LFOs, musical sequences, randomisation, etc... Some functions will soon be added to make written these less verbose. For now, you are on your own!

Temporal recursive functions have only one drawback: they NEED a `delay` argument that must be an `int`. Without a `delay`
