![sardine](pictures/sardine.png)
# Sardine
Python based live coding library with MIDI and OSC support ✨


- [Sardine](#sardine)
  - [Elevator Pitch](#elevator-pitch)
  - [Installation](#installation)
    - [Sardine Python Package](#sardine-python-package)
    - [SuperCollider & SuperDirt](#superdirt)
    - [Code-editing with Sardine](#code-editing-with-sardine)
  - [Debug](#debug)
    - [Known bugs and issues](#known-bugs-and-issues)
  - [Usage](#usage)
    - [Configuration Tools](#configuration-tools)
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

Sardine is a Python library tailored for musical live coding. It is based on the principle of [temporal recursion](http://extempore.moso.com.au/temporal_recursion.html). Sardine allows the execution of recursive functions in musical time. It means that you can sequence synthesizers, samples, MIDI and OSC signals or even arbitrary Python code with a strict timing! Sardine is also able to piggy-back on the [SuperDirt](https://github.com/musikinformatik/SuperDirt) audio engine, a famous backend used by many live coders worldwide.

Sardine can turn Python into a very fruitful musical instrument or stage control tool for electronic musicians.

The library is a bit rough on the edges. I made it public in order to share it easily and to encourage collaboration! **Sardine is looking for contributors**. Here are the goals for a first public release:

* [X] Solid timing system allowing the execution and synchronisation of temporal recursive functions.
* [X] Easy and simple to use MIDI/OSC and SuperDirt API.
* [X] MIDIIn/OSCIn for tweaking functions live using controllers and other devices.
* [X] Configuration scripts / tools
* [ ] Solid and interesting patterning systems for musical parameters
* [ ] Documentation / Wiki / Easy install process: quality of life for users.
* [ ] Technical documentation: helping devs and contributors :).

## Installation

### Sardine Python Package

The installation process is fairly simple if you wish to install Sardine system-wide. You will need, that goes without saying, the most recent version of Python you can install on your OS. Some knowledge of the usage of a command prompt/shell is required but only for the installation / configuration process.

0) install **Python** (3.9/3.10) and a suitable code editor ([VSCode](https://code.visualstudio.com/), [Vim](https://www.vim.org/)/[Neovim](https://neovim.io/), [Emacs](https://www.gnu.org/software/emacs/), etc..)
1) run `git clone https://github.com/Bubobubobubobubo/Sardine` to download Sardine.
2) run `cd sardine && pip3 install -e .` (can also be `python` on some systems).
   - **You need to have `python` and `pip` already installed on your computer**.
   - **Run the `git clone` commnad wherever you like**.
   - optionally (but recommended), run `pip3 install uvloop` (MacOS/Linux only).
3) open a new interactive session using `python3 -m asyncio`
   - **/!\\ Make sure that you are running the asyncio REPL!**
   - **/!\\ The `IPython` REPL will not work. It is handling `asyncio` code differently.
4) import the library `from sardine import *`
5) Follow the prompt to connect to a MIDI Output. You will be able to configure the default MIDI interface later.
6) Configure Sardine to your liking with `sardine-config`, `sardine-config-superdirt` and `sardine-config-python`.
7) Read the examples provided in the `examples/` folder to learn more.
   - **/!\\ Some examples might be out of date in the early stages of the project** 

### SuperDirt

SuperDirt is a nice to have but **optional** output for Sardine. It is a well-known audio engine used by live coders, originally developed by Julian Rohrhuber for [TidalCycles](https://tidalcycles.org/). It provides a simple message-based syntax to speak with SuperCollider, to trigger samples, synthesizers and many other things.

1) Refer to the [SuperDirt](https://github.com/musikinformatik/SuperDirt) installation guide for your platform. It will guide you through the installation of [SuperCollider](https://supercollider.github.io/) and **SuperDirt** for your favorite OS. It is usually a three step process:
    * install [SuperCollider](https://supercollider.github.io/).
    * run `Quarks.install("SuperDirt")` in the SCIDE window.
    * run `SuperDirt.start` to start the engine.

We will assume that you already have some experience dealing with SuperDirt in order to focus more on explaining how **Sardine** works. **Sardine** will assume that `SuperCollider` (and more specifically `sclang`) is accessible on your `$PATH`. Everything should run just fine if you install it in the default folder for your platform. **Sardine** will automatically try to boot a **SuperCollider** server and the `SuperDirt` audio engine as soon as you import the library.

### Code-editing with Sardine

You can use `Sardine` directly from the Python interpreter. There is nothing wrong about it, but you will be pretty limited in what you can do. It is sometimes enough to run quick tests. After a while, you will figure out that working this way is fairly cumbersome and you will likely be searching for a better text editor. **Sardine** code can become quite verbose when dealing with complex *swimming* functions.

As you might have guessed already, there is no `Sardine` plugin for VSCode, Atom or any popular code editor. However, **Sardine** is Python and there are great plugins to deal with interactive code. Here are a few things you can try:
* [Vim](https://github.com/vim/vim) or [Neovim](https://github.com/neovim/neovim) [slime](https://github.com/jpalardy/vim-slime) plugin. This plugin gives you the ability to `pipe` strings from a text buffer to another (from your code to another buffer containing the python interpreter). 
* VSCode with the [Jupyter Notebook](https://jupyter.org/) extension
    - install VSCode and the Jupyter Notebook plugin. Create a new `.ipynb` notebook.
    - make sure that you are using the right Python version as your kernel (3.9 / 3.10).
    - run `%pip install -e "path/to/sardine"`, restart the kernel when `pip` is done installing.!
    - run `from sardine import *` and have fun!
* Emacs with the [python.el](https://github.com/emacs-mirror/emacs/blob/master/lisp/progmodes/python.el) plugin.

## Debug

Please provide feedback on the installation process! I try to document it as much as I can but I lack feedback on the installation process on different systems, etc.. You might also have different use cases that I might not have anticipated.

### Known bugs and issues

* **[WINDOWS ONLY]**: `uvloop` does not work on Windows. Fortunately, you can still run **Sardine** but don't expect the tempo/BPM to be accurate. You will have to drastically slow down the clock for it to work (~20bpm is a safe value)! This might be linked to a different implementation of `asyncio` on Windows.

* **[LINUX/MACOS]**: `pip3 install` fails on `python-rtmidi build`. Its probably because the `libjack-dev` lib is missing. You can install it with `sudo apt-get install libjack-dev` on Debian based systems, with `brew` for MacOS, and with `pacman` for any other Arch-based system.

## Configuration Tools

When you boot Sardine for the first time, **Sardine** will create its own configuration folder and configuration files. The path will be printed everytime time you boot **Sardine** thereafter. There are three files you can tweak and configure:
- `config.json`: main **Sardine** configuration file.
- `default_superdirt.scd`: **SuperDirt** configuration file.
- `synths` folder: store new synthesizers written with **SuperCollider**.

The location of the configuration folder is assumed to be the best possible default location based on your OS:
- **MacOS**: `Users/xxx/Library/Application\ Support/Sardine/`
* **Linux**: `.config` folder (???).
* **Windows**: `%appdata%/Sardine` (???).

The `config.json` file will allow you to finetune **Sardine** by choosing a default MIDI port, a default PPQN and BPM, etc... The `default_superdirt.scd` is your default `SuperDirt` configuration. You must edit it if you are willing to load more audio samples, change your audio outputs or add anything that you need on the SuperCollider side. The `synths` folder is a repository for your `SynthDefs` file. Each synthesizer should be saved in its own file and will be loaded automatically at boot-time.

There is another file, `user_configuration.py` that is not created by default. It must be added manually if you wish to use this feature. All the code placed in this file will be imported by default everytime you boot **Sardine**. It is an incredibely useful feature to automate some things:
* custom user-made functions and aliases.
* Sardine running in "art installation" mode.

**Sardine** will be installed along with configuration tools that are meant to make configuration easy and fast. They will be automatically installed on your `$PATH`:
- `sardine-config` is a CLI meant to edit `config.json` from the command-line.
- `sardine-config-python` will fire `$EDITOR` to config `user_configuration.py`.
- `sardine-config-superdirt` will fire `$EDITOR` to config `default_superdirt.scd`.

Sardine will have to be runned at least once for the `config.json` file to be created. 

## Usage

### The internal Clock

As soon as the library is imported (`from sardine import *`), an instance of `Clock` will start to run in the background and will be referenced by the variable `c`. `Clock` is the main MIDI Clock. By default, this clock is running in `active` mode: it will send a MIDI clock signal every tick on the default MIDI port. It can also be `passive` and listen to the default MIDI port if you prefer. Don't override the `c` variable. You won't have to worry a lot about the internals. Just remember that some methods can be used to maximize the fun you get:

* `c.bpm`: current BPM (beats per minute).
* `c.ppqn`: current [PPQN](https://en.wikipedia.org/wiki/Pulses_per_quarter_note) (Pulses per Quarter Note, used by MIDI gear).
  - be careful. The tempo might fluctuate based on the PPQN you choose. Assume that 24 is a default sane PPQN for most synthesizers/drum machines.

`c.bpm` and `c.ppqn` can be manually adjusted if you feel like it. Be careful, changing these values can result in a dramatic tempo shift.

The Clock can either be `active` or `passive`. The `active` Clock will emit a Clock signal on the MIDI port you picked by default. The `passive` Clock will await for a MIDI Clock signal coming from elsewhere (DAWs, hardware, other softwares..). Sardine will not behave nicely if no external clock is running while in `passive` mode. Being able to send a MIDI Clock Out or to receive a MIDI Clock In is great for collaborating with other musicians. Live is also able to mirror an Ableton Link clock to a MIDI Clock.

[TODO: clock attributes and temporal helpers]

### Temporal recursive functions

In **Sardine** parlance, a **swimming function** is a function that is scheduled to be repeated by recursion. To define a function as a **swimming function**, use the `@swim` decorator. The opposite of the `@swim` decorator is the `@die` decorator that will release a function from recursion.

```python
@swim # replace me by 'die'
def bd(d=1):
    """Loud bass drum"""
    S('bd', amp=2).out()
    anew(bd, d=1) # anew == again == cs
```

If you don't manually add the recursion to the designated **swimming function**, the function will run once and stop. Recursion must be explicit!

```python
# Boring
@swim 
def bd(d=1):
    S('bd', amp=2).out()
```

The recursion can (and should) be used to update your arguments between each call of the **swimming function**. Here is an example of a very simple iterator:

```
@swim # or die 
async def iter(d=1, nb=0):
    """A simple recursive iterator"""
    print(f"{nb}")
    anew(iter, d=1, nb=nb+1)
# 0
# 1
# 2
# 3
# 4
```

This is an incredibly useful feature to keep track of state between each call of your function. **Swimming functions** are helpful tools that can be used to produce very musical results! Temporal recursion makes it very easy to manually code LFOs, musical sequences, randomisation, etc... Some functions will soon be added to make some of these less verbose for the end-user. For now, you are (almost) on your own!

**Swimming functions** are great but they have one **BIG** difference compared to a classic temporal recursion: they are *temporal* recursive. They must be given a `delay` argument. The `delay` argument is actually `d` (short is better). If you don't provide it, Sardine will assume that your function uses `d=1`.

### Triggering sounds / samples / synthesizers

The easiest way to trigger a sound with `Sardine` is to send an OSC message to `SuperDirt`. Most people will use this output instead of plugging multiple synthesizers listening to MIDI or crafting OSC listeners. The interface to SuperDirt is very crude but fully functional. By default, **Sardine** will attempt to boot with its own `SuperCollider` and `SuperDirt` configuration. You can disable this by changing the configuration: `sardine-config --boot False`.
* **default:** `SuperDirt` will be booted everytime the library is imported.
* **manual:** `SuperDirt` (and `SuperCollider`) needs to be booted independently on the default port (`57120`).

People familiar with [TidalCycles](https://tidalcycles.org/) will feel at home using the `S()` (for `SuperDirt`) object. It is a simple object made for composing SuperDirt messages:

```python
# A bassdrum (sample 0 from folder 'bd')
S('bd').out() 
# Fourth sample, way louder!
S('bd', n=3, amp=2).out() 
# Patterning a parameter (read the appropriate section) 
S('bd', n=3, amp=1, speed='1 0.5').out(i) 
# Introducing some Python in our parameters
S('bd' if random() > 0.5 else 'hh', speed=randint(1,5)) 
```

Notice the `.out()` method used on the `S`(ound) object? That's because `S` can be modified and composed before being sent out. You can take time to develop your functions, add conditions, etc... When you are ready to send a sound, just use the `.out()` method:

```python
@swim
def indirect_bd(d=1, speed=1):
    a = S('bd')
    a.speed(4)
    a.out()
    anew(indirect_bd, d=1, speed=randint(1, 5))
```

Be careful not to override the method by changing an individual parameter (`a.speed=5`). It is a method, you **must** use parentheses! Seems cumbersome but you will like it when you will start to get into method chaining like so:

```python
S('bd').shape(random()).speed(randint(1,4))
```

## MIDI

`Sardine` supports all the basic messages one can send and receive through MIDI, but will support many more in the future.

### MIDI Out

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

### MIDI In

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

You can send OSC (**Open Sound Control**) messages by declaring your own OSC connexion and sending custom messages. It is very easy to do so. Take a look at the following example:

```python
from random import randint, random, chance

# Open a new OSC connexion
my_osc = OSC(ip="127.0.0.1",
        port= 23000, name="Bibu",
        ahead_amount=0.25)

# Recursive function sending OSC
@swim
async def custom_osc(delay=1):
    my_osc.send(c, '/coucou', [randint(1,10), randint(1,100)])
    cs(custom_osc, delay=1)

# Closing and getting rid of the connexion

cr(custom_osc)

del my_osc
```

Note that you need to provide the clock as the first argument of the `send()` method. It is probably better to write a dedicated function to avoid having to specify the address everytime you want to send something at a specific address:

```python
def coucou(*args): my_osc.send(c, '/coucou', list(args))
```

## Crash

By coding live, you will soon make mistakes. There is currently no recovery mechanism from a typing/coding error. The function will stop dramatically, leaving you with only silence. A recovery mechanism is on the way, warning you of any mistake you made and feeding an older version of your function instead of your defective one.

## Development

**Sardine* uses [The Black Code Style](https://black.readthedocs.io/en/stable/the_black_code_style/index.html). 

To enforce this code style you must run [black](https://github.com/psf/black):
```shell
black .
```