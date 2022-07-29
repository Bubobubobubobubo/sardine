# Sardine

## Overview


Sardine is a fun summer project I am currently working on, based on Python 3.10 `asyncio` library. Sardine is a live coding library exploring the idea of temporal recursion. It is capable of sending a MIDI Clock to external softwares and synthesizers. It can also piggy-back on the [SuperDirt](https://github.com/musikinformatik/SuperDirt) audio engine to trigger or sequence samples, synthesizers, custom DSP and much more things :). Because `Sardine` is fairly simple and barebones, you can also use it to schedule the execution of custom Python functions on a musical clock!

I am indexing my work on this repository but the library is not yet usable / released. I made it public in order to share it without having to add contributors every time. You are also welcome to make pull requests if you think that you can bring something new!

## Installation

### Sardine Python Package

The installation process is fairly simple:
1) run `setup.py` using `pip3 install -e .` to download required libraries and install the library.
   - **You need to have `python` and `pip` already installed on your computer**.
2) open a new interactive session using `python3 -m asyncio`
   - **/!\\ Make sure that you are running the asyncio REPL!**
3) import the library `from sardine import *`
4) Follow the prompt to connect to a MIDI Output.
5) Read the examples provided in the `examples/` folder to learn more.

### SuperDirt

1) Refer to the [SuperDirt]() installation guide for your platform. It will guide you through the installation of [SuperCollider]() and **SuperDirt** for your favorite OS.

### Code-editing with Sardine

You can use `Sardine` directly from the Python interpreter. There is nothing wrong about it. After a while, you will figure out that it is fairly cumbersome and you will likely be searching for a better text editor. As you might have guessed already, there is no `Sardine` plugin for VSCode, Atom or any popular code editor. The easiest way to use it is by using Vim[]() or Neovim[]() [slime]() plugin. This plugin gives you the ability to `pipe` strings from a text buffer to another (from your code to another buffer containing the python interpreter). Any software providing the same functionality will likely work (VSCode Python plugins, notebooks, etc...).

## Debug

`Sardine` is crippled with bugs. I am developing `Sardine` for my own usage right now. Some configuration variables might still refer to my own local environment... some packages might need to be installed manually if you encounter an error. Please provide feedback on the installation process!

## Usage

### The internal Clock

As soon as the library is imported (`from sardine import *`), an instance of `Clock` will start to run in the background and will be referenced to by the variable `c`. `Clock` is the main MIDI Clock you will be playing with. Don't override the `c` variable. You won't have to worry a lot about the internals. Just remember that some methods could be used for fun:
* `c.bpm`: current BPM (can be inexact depending on your `ppqn`)
* `c.ppqn`: current [PPQN](https://en.wikipedia.org/wiki/Pulses_per_quarter_note) (1-??).
  - be careful. The tempo might fluctuate based on the PPQN you choose.
* `c.get_tick_duration`: duration of a clock tick.

`c.bpm` and `c.ppqn` can be manually adjusted if you feel like it. Be careful, changing these values can result in a dramatic tempo shift. I still need to work a little bit on the internals to make this correct :). For now, the clock is limited to MIDI output only. It means that you can open a DAW such as Ableton or Bitwig and use `Sardine` as your MIDI Clock. MIDI Clock In is a feature I still need to code in :) and is not yet supported.

There are some sugared methods to schedule coroutines on the clock:
- `cs` (`c.schedule(coro)`): introduce a new coroutine.
- `cr` (`c.remove(coro)`): remove a coroutine.

**Example:**
```python3
cs(my_super_bass_drum(delay(50)))
cs(hatty_hat(delay(100)))

# Bored
cr(my_super_bass_drum)
cr(hatty_hat)
```

More functions will be added to take care of scheduling on the clock. I still have some issues to fix with `asyncio`.

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

Temporal recursive functions have only one drawback: they NEED a `delay` argument that must be an `int`. Without this argument, `Sardine` will likely crash. This `delay` can be modified every loop in order to create rhythms but you need to provide an initial `delay`.

### Triggering sounds / samples / synthesizers

So far so good, you
