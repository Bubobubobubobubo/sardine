![sardine](pictures/sardine.png)
# Sardine
Livecoding in python with MIDI and OSC support ✨


- [Sardine](#sardine)
  - [Elevator Pitch](#elevator-pitch)
  - [Installation](#installation)
    - [Sardine Python Package](#sardine-python-package)
    - [SuperCollider & SuperDirt](#superdirt)
    - [Code-editing with Sardine](#code-editing-with-sardine)
  - [Debug](#debug)
    - [Known bugs and issues](#known-bugs-and-issues)
  - [Usage](#usage)
    - [Clock and Scheduling System](#the-internal-clock)
    - [Usage as a generic MIDI Clock](#usage-as-a-generic-midi-clock)
    - [Temporal recursive functions](#temporal-recursive-functions)
    - [Triggering sounds / samples / synthesizers](#triggering-sounds--samples--synthesizers)
  - [MIDI](#midi)
    - [MIDI Out](#midi-out)
    - [MIDI In](#midi-in)
  - [OSC](#osc)
  - [Crash](#crash)
  - [Troubleshooting](#troubleshooting)

## Elevator Pitch

Sardine is a Python library made for musical live coding. It is based on a specific type of recursion, the [temporal recursion](http://extempore.moso.com.au/temporal_recursion.html). Sardine allows the execution of recursive functions in musical time. It means that you can sequence synthesizers, samples, MIDI and OSC signals or even arbitrary Python code with a strict timing! Sardine is also able to piggy-back on the [SuperDirt](https://github.com/musikinformatik/SuperDirt) audio engine, a famous backend used by many live coders worldwide.

The library is far from being usable by unexperienced users. I made it public in order to share it easily and to encourage collaboration! **Sardine is looking for contributors**. Here are the goals for a first public release:

* [x] Solid timing system allowing the execution and synchronisation of temporal recursive functions.
* [ ] Easy and simple to use MIDI/OSC and SuperDirt API.
* [ ] MIDIIn/OSCIn for tweaking functions live using controllers and other devices.
* [ ] Complete API targetting the `SuperDirt` sound engine.

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

Sardine will assume that `SuperCollider` (and more specifically `sclang`) is accessible on your PATH. Everything should run just fine if you install it in the default folder for your platform. Sardine will automatically try to boot a SuperCollider server and the `SuperDirt` audio engine as soon as you import the library.

### Code-editing with Sardine

You can use `Sardine` directly from the Python interpreter. There is nothing wrong about it. After a while, you will figure out that it is fairly cumbersome and you will likely be searching for a better text editor. `Sardine` code can become quite verbose when dealing with complex *swimming* functions.

As you might have guessed already, there is no `Sardine` plugin for VSCode, Atom or any popular code editor. The easiest way to use it is by using [Vim](https://github.com/vim/vim) or [Neovim](https://github.com/neovim/neovim) [slime](https://github.com/jpalardy/vim-slime) plugin. This plugin gives you the ability to `pipe` strings from a text buffer to another (from your code to another buffer containing the python interpreter). Any software providing the same functionality will likely work (VSCode Python plugins, notebooks, etc...). VSCode is assumed to work very well for editing Sardine code as well.

## Debug

Please provide feedback on the installation process! Everything is pretty new so I might not be able to anticipate how `Sardine` will run on your computer. I am discovering new bugs and corner-cases everyday, and I would love to fix them to get a stable release soon :)

### Known bugs and issues

* **[WINDOWS ONLY]**: `uvloop` doesn't work on Windows. Fortunately, you can still run `Sardine` but don't expect the tempo/BPM to be accurate. You will have to drastically slow down the clock for it to work (~20bpm is a safe value)! This might be linked to a different implementation of `asyncio` on Windows.

* **[LINUX/MACOS]**: `pip3 install` fails on `python-rtmidi build`. Its probably because the `libjack-dev` lib is missing. You can install it with `sudo apt-get install libjack-dev` on Debian based systems, with `brew` for MacOS, and with `pacman` for any other Arch-based system.

## Usage

### The internal Clock

As soon as the library is imported (`from sardine import *`), an instance of `Clock` will start to run in the background and will be referenced by the variable `c`. `Clock` is the main MIDI Clock you will be playing with. Don't override the `c` variable. You won't have to worry a lot about the internals. Just remember that some methods can be used to maximize the fun you get:
* `c.bpm`: current BPM
* `c.ppqn`: current [PPQN](https://en.wikipedia.org/wiki/Pulses_per_quarter_note)
  - be careful. The tempo might fluctuate based on the PPQN you choose.

`c.bpm` and `c.ppqn` can be manually adjusted if you feel like it. Be careful, changing these values can result in a dramatic tempo shift.

There are some sugared methods to schedule coroutines on the clock:
- `cs` (`c.schedule(coro, *args, **kwargs)`): introduce a new coroutine.
- `cr` (`c.remove(coro, *args, **kwargs)`): remove a coroutine.

**Example:**
```python3
cs(my_super_bass_drum, delay=2)
cs(hatty_hat, delay=0.5)

# Bored
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

The Clock can either be `active` or `passive`. The `active` Clock will emit a Clock signal on the MIDI port you picked by default. The `passive` Clock will await for a MIDI Clock signal coming from elsewhere (DAWs, hardware, other softwares..). Sardine will not behave nicely if no external clock is running while in `passive` mode. Being able to send a MIDI Clock Out or to receive a MIDI Clock In is great for collaborating with other musicians. Live is also able to mirror an Ableton Link clock to a MIDI Clock.

### Temporal recursive functions

Asynchronous functions can be scheduled to run periodically on the clock and support temporal recursion! It means that you can write the following and expect the following output:

```python
# A basic temporal recursive function
async def incr(delay=20, num=0):
    num += 1
    print(f"Num: {num}")
    cs(num, delay=20, num)

# Scheduling it on the clock
cs(num, delay=20, num=0)

# Output
# Num: 1
# Num: 2
# Num: 3
# Num: 4
# Num: 5
```

This is an incredibely useful feature to keep track of state between iterations of your function. Sardine users refer to these functions as **swimming functions**. They have some nice musical implications as well! Temporal recursion makes it very easy to manually code LFOs, musical sequences, randomisation, etc... Some functions will soon be added to make these less verbose for the end-user. For now, you are on your own!

Temporal recursive functions have only one drawback: they NEED a `delay` argument. If you don't provide it, `Sardine` will default to using `delay=1`, a quarter note.

### Triggering sounds / samples / synthesizers

The easiest way to trigger a sound with `Sardine` is to send an OSC message to `SuperDirt`. Sardine can either boot its own `SuperDirt` instance or let you do it if you are willing to:
- **Default:** `SuperDirt` will be booted everytime the library is imported.
- **Manual:** `SuperDirt` (and `SuperCollider`) needs to be booted independently on the default port (`57120`).

The configuration file, automatically created the first time you boot Sardine, can help you to tune the defaults.

The `SuperDirt` object is your main interface to `SuperDirt`. The syntax is nice and easy and wil remind you of *TidalCycles* if you are already familiar with it. `SuperDirt` has been aliased to `S` to make it easier to type.

```python
S('bd').out() # a bassdrum (sample 0 from folder 'bd')
S('bd', n=3, amp=2).out() # third sample, way louder
S('bd', n=3, amp=1, speed=[0.5,1]).out() # third sample, played twice at different speeds
S('bd' if random() > 0.5 else 'hh', speed=randint(1,5)) # Python shenanigans
```

The simplest function you can write using `Sardine` is probably a simple bassdrum:

```python
@swim
def bd(delay=1):
    S('bd').out()
    cs(bd, delay=1)
```

You can be more playful and do something by toying with temporal recursion:


```python
@swim
def bd(delay=1, speed=1):
    S('bd').out()
    cs(bd, delay=1, speed=randint(1, 5))
```

Notice the `.out()` method used on the `S`(ound) object? That's because `S` can be modified and composed before being send out. You can take time to develop your functions, add conditions, etc... When you are ready to send the sound out, just use the `.out()` method:


```python
@swim
def indirect_bd(delay=1, speed=1):
    a = S('bd')
    a.speed(4)
    a.out()
    cs(indirect_bd, delay=1, speed=randint(1, 5))
```

Be careful not to override the method by changing an individual parameter (`a.speed=5`). It is a method, you **must** use parentheses! Seems cumbersome but you will like it when you will start to get into method chaining like so:

```python
S('bd').shape(random()).speed(randint(1,4))
```

## MIDI

`Sardine` supports all the basic messages one can send and receive through MIDI, but will support many more in the future.

### MIDI Out

Here is an exemple of a **swimming function** sending a constant MIDI Note:

```python
@swim
def midi_tester(delay=1):
    note(
        duration=1,
        note=60,
        velocity=127,
        channel=0)
    cs(midi_tester, delay=1)
```

Note that the channel count starts at `0`, covering a range from `0` to `15`. The duration for each every note should be written in milliseconds(`ms`) because MIDI is handling MIDI Notes as two separate messages (`note_on` and `note_off`).

Let's go further and make an arpeggio using the same technique:

```python
from itertools import cycle
arpeggio = cycle([60, 64, 67, 71])
@swim
def midi_tester(delay=0.25):
    note(1, next(arpeggio), 127, 1)
    cs(midi_tester, delay=0.25)
```

A similar function exists for sending MIDI CC messages. Let's combine it with our arpeggio:

```python
from itertools import cycle
from random import randint
arpeggio = cycle([60, 64, 67, 71])
@swim
def midi_tester(delay=0.25):
    note(1, next(arpeggio), 127, 1)
    cc(channel=1, control=20, value=randint(1,127))
    cs(midi_tester, delay=0.25)
```

### MIDI In

MIDIIn is supported through the use of a special object, the `MidiListener` object. This object will open a connexion listening to incoming MIDI messages. There are only a few types of messages you should be able to listen to:
* MIDI Notes through the `NoteTarget` object
* MIDI CC through the `ControlTarget` object

Additionally, you can listen to incoming Clock messages (`ClockListener`) but you must generally let Sardine handle this by itself.

Every `MidiListener` is expecting a target. You must declare one and await on it using the following syntax:

```python
a = MidiListener(target=ControlTarget(20, 0))

from random import random
@die
def pluck(delay=0.25):
    S('pluck', midinote=a.get()).out()
    cs(pluck, delay=0.25)
```

In this example, we are listening on CC n°20 on the first midi channel (`0`), on the default MIDI port. Sardine cannot assert the value of a given MIDI Control before it receives a first message, so the initial value will be assumed to be `0`.

You can fine tune your listening object by tweaking the parameters:

```python
# picking a different MIDI Port
a = MidiListener('other_midi_port', target=ControlTarget(40, 4))
```

## OSC

You can send OSC (Open Sound Control) messages by declaring your own OSC connexion and sending custom messages. It is very easy to do so. Take a look at the following example:

```python
from random import randint, random, chance

# Open a new OSC connexion
my_osc = OSC(ip="127.0.0.1",
        port= 23000, name="Bibu",
        ahead_amount=0.25)

# Recursive function sending OSC
@swim
async def custom_osc(delay=1):
    my_osc.send('/coucou', [randint(1,10), randint(1,100)])
    cs(custom_osc, delay=1)

# Closing and getting rid of the connexion

cr(custom_osc)

del my_osc
```

## Crash

By coding live, you will soon make mistakes. There is currently no recovery mechanism from a typing/coding error. The function will stop dramatically, leaving you with only silence. A recovery mechanism is on the way, warning you of any mistake you made and feeding an older version of your function instead of your defective one.
