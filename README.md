![sardine](pictures/sardine.png)

[Getting Started](#installation) - [Usage](#usage)

## Elevator Pitch

Sardine is a Python library made for musical live coding. It is based on a specific type of recursion, the [temporal recursion](http://extempore.moso.com.au/temporal_recursion.html). Sardine allows the execution of recursive functions in musical time. It means that you can sequence synthesizers, samples, MIDI and OSC signals or even arbitrary Python code! Sardine is also able to piggy-back on the [SuperDirt](https://github.com/musikinformatik/SuperDirt) audio engine, a famous backend used by many live coders worldwide.

The library is far from being usable by random users. I made it public in order to share it easily and to encourage collaboration! Here are the goals for a first public release:

* Solid timing system allowing the execution and synchronisation of temporal recursive functions.
* Easy and simple to use MIDI/OSC and SuperDirt API.
* MIDIIn/OSCIn for tweaking functions live using controllers and other devices.

## Installation

### Sardine Python Package

The installation process is fairly simple:

1) run `setup.py` using `pip3 install -e .` to download required libraries and install the library.
   - **You need to have `python` and `pip` already installed on your computer**.
2) open a new interactive session using `python3 -m asyncio`
   - **/!\\ Make sure that you are running the asyncio REPL!**
   - **/!\\ The `IPython` REPL will not work. It is handling asyncio code differently.
3) import the library `from sardine import *`
4) Follow the prompt to connect to a MIDI Output.
5) Read the examples provided in the `examples/` folder to learn more.

### SuperDirt

1) Refer to the [SuperDirt](https://github.com/musikinformatik/SuperDirt) installation guide for your platform. It will guide you through the installation of [SuperCollider](https://supercollider.github.io/) and **SuperDirt** for your favorite OS. It is usually a three step process:
    * install SuperCollider.
    * run `Quarks.install('SuperDirt')` in the SCIDE window.
    * run `SuperDirt.start` to start the engine.

### Code-editing with Sardine

You can use `Sardine` directly from the Python interpreter. There is nothing wrong about it. After a while, you will figure out that it is fairly cumbersome and you will likely be searching for a better text editor. `Sardine` code can become quite verbose when dealing with complex functions.

As you might have guessed already, there is no `Sardine` plugin for VSCode, Atom or any popular code editor. The easiest way to use it is by using [Vim](https://github.com/vim/vim) or [Neovim](https://github.com/neovim/neovim) [slime](https://github.com/jpalardy/vim-slime) plugin. This plugin gives you the ability to `pipe` strings from a text buffer to another (from your code to another buffer containing the python interpreter). Any software providing the same functionality will likely work (VSCode Python plugins, notebooks, etc...).

## Debug

Please provide feedback on the installation process! Everything is pretty new so I might not be able to anticipate how `Sardine` will run on your computer.

## Usage

### The internal Clock

As soon as the library is imported (`from sardine import *`), an instance of `Clock` will start to run in the background and will be referenced to by the variable `c`. `Clock` is the main MIDI Clock you will be playing with. Don't override the `c` variable. You won't have to worry a lot about the internals. Just remember that some methods could be used for fun:
* `c.bpm`: current BPM (can be inexact depending on your `ppqn`)
* `c.ppqn`: current [PPQN](https://en.wikipedia.org/wiki/Pulses_per_quarter_note) (1-??).
  - be careful. The tempo might fluctuate based on the PPQN you choose.

`c.bpm` and `c.ppqn` can be manually adjusted if you feel like it. Be careful, changing these values can result in a dramatic tempo shift. I still need to work a little bit on the internals to make this correct :). For now, the clock is limited to MIDI output only. It means that you can open a DAW such as Ableton or Bitwig and use `Sardine` as your MIDI Clock. MIDI Clock In is a feature I still need to code in :) and is not yet supported.

There are some sugared methods to schedule coroutines on the clock:
- `cs` (`c.schedule(coro, *args, **kwargs)`): introduce a new coroutine.
- `cr` (`c.remove(coro, *args, **kwargs)`): remove a coroutine.

**Example:**
```python3
cs(my_super_bass_drum, delay=2)
cs(hatty_hat, delay=0.5)

# Bored
cr(my_super_bass_drum)
cr(hatty_hat)
```

This is nice and everything but still a bit long to type on-the-fly while you are on stage. You might prefer using the `@swim` and `@die` decorators:
```python
@swim
async def bd(delay=1):
    """ A simple bass drum """
    dur = choice([2, 1])
    S('bd', amp=2).out()
    cs(bd, delay=dur)


@die
async def iter(delay=1, nb=0):
    """ A simple recursive iterator """
    nb += 1
    print(f"{nb}")
    cs(iter, delay=1, nb=nb+1)
```

### Temporal recursive functions

Asynchronous functions can be scheduled to run periodically on the clock and support temporal recursion! It means that you can write the following and expect the following output:

```python
# A basic temporal recursive function
async def incr(delay=20, num=0):
    num += 1
    print(f"Num: {num}")
    cs(num, delay=20, num)

# Scheduling it on the clock
cs(num, delay=20, num=0)

# Output
# Num: 1
# Num: 2
# Num: 3
# Num: 4
# Num: 5
```

This is an incredibely useful feature to keep track of state between iterations of your function. It has some musical implications as well! Temporal recursion makes it very easy to manually code LFOs, musical sequences, randomisation, etc... Some functions will soon be added to make written these less verbose. For now, you are on your own!

Temporal recursive functions have only one drawback: they NEED a `delay` argument. If you don't provide it, `Sardine` will default to using `delay=1`, a quarter note.

### Triggering sounds / samples / synthesizers

The easiest way to trigger a sound with `Sardine` is to send an OSC message to `SuperDirt`. `SuperDirt` must be booted separately from `Sardine`. The `Sound` object can be used to do so. The syntax is nice and easy and wil remind you of TidalCycles if you are already familiar with it. `Sound` as been aliased to `S` to make it easier to type.

```python
S('bd').out() # a bassdrum (sample 0 from folder 'bd')
S('bd', n=3, amp=2).out() # third sample, way louder
S('bd', n=3, amp=1, speed=[0.5,1]).out() # third sample, played twice at different speeds
S('bd' if random() > 0.5 else 'hh', speed=randint(1,5)) # Python shenanigans
```

The simplest function you can write using `Sardine` is probably a simple bassdrum:

```python
async def bd(delay=1):
    S('bd').out()
    cs(bd, delay=1)
cs(bd, delay=1)
```

You can be more playful and do something by toying with temporal recursion:


```python
async def bd(delay=1, speed=1):
    S('bd').out()
    cs(bd, delay=1, speed=randint(1, 5))
cs(bd, delay=1, speed=1)
```

Notice the `.out()` method used on the `S`(ound) object? That's because `S` can be modified and composed before being send out. You can take time to develop your functions, add conditions, etc... When you are ready to send the sound out, just use the `.out()` method:


```python
async def indirect_bd(delay=1, speed=1):
    a = S('bd')
    a.speed = speed
    a.out()
    cs(indirect_bd, delay=1, speed=randint(1, 5))
cs(indirect_bd, delay=1, speed=1)
```

Not all parameters are currently available. SuperDirt parameters have been hardcoded... This should be easy to fix but I never took time to do it properly.

## Crash

By coding live, you will soon make mistakes. There is currently no recovery mechanism from a typing/coding error. The function will stop dramatically, leaving you with only silence. A recovery mechanism is on the way, warning you of any mistake you made and feeding an older version of your function instead of your defective one.
