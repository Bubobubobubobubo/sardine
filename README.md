![sardine](pictures/sardine.png)
# Sardine: Python based live coding library with MIDI and OSC support ✨

Sardine is a Python library tailored for musical live coding. **Sardine** can turn Python into a fun and fruitful music instrument or stage control tool for electronic musicians. It is based on the principle of [temporal recursion](http://extempore.moso.com.au/temporal_recursion.html). Sardine allows the execution of recursive functions in musical time. It means that you can sequence synthesizers, samples, MIDI and OSC signals or even arbitrary Python code with a strict timing! Sardine is also able to piggy-back on the [SuperDirt](https://github.com/musikinformatik/SuperDirt) audio engine, a famous backend used by many live coders worldwide. The library is still a bit rough on the edges. I decided to publish it in order to share it easily and to encourage collaboration! **Sardine is looking for contributors**. Here are the goals for a first public release:

* [X] Solid timing system allowing the execution and synchronisation of temporal recursive functions.
* [X] Easy and simple to use MIDI/OSC and SuperDirt API.
* [X] MIDIIn/OSCIn for tweaking functions live using controllers and other devices.
* [X] Configuration scripts / tools
* [ ] Interesting patterning system for musical parameters
* [ ] Documentation / wiki / easy install process: quality of life for users.
* [ ] Technical documentation: helping devs and contributors :).



- [Installation and configuration](#installation)
  - [Sardine Python Package](#sardine-python-package)
  - [SuperCollider & SuperDirt](#superdirt)
  - [Code-editing with Sardine](#code-editing-with-sardine)
  - [Known bugs and issues](#known-bugs-and-issues)

- [Using Sardine](#using-sardine)
  - [Configuration and Config Tools](#configuration-and-config-tools)
  - [Clock and Scheduling System](#the-internal-clock)
  - [What does sleep really mean?](#what-does-sleep-really-mean)
  - [Temporal recursive functions](#temporal-recursive-functions)
  - [Triggering sounds / samples / synthesizers](#triggering-sounds--samples--synthesizers)
  - [Composing patterns](#composing-patterns)
    - [Sardine Grammar](#sardine-grammar)
- [MIDI](#midi)
  - [MIDI Out](#midi-out)
  - [MIDI In](#midi-in)
- [OSC](#osc)
- [Crash](#crash)
- [Troubleshooting](#troubleshooting)

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
## Known bugs and issues

Please provide feedback on the installation process! I try to document it as much as I can but I lack feedback on the installation process on different systems, etc.. You might also have different use cases that I might not have anticipated.

* **[WINDOWS ONLY]**: `uvloop` does not work on Windows. Fortunately, you can still run **Sardine** but don't expect the tempo/BPM to be accurate. You will have to drastically slow down the clock for it to work (~20bpm is a safe value)! This might be linked to a different implementation of `asyncio` on Windows.

* **[LINUX/MACOS]**: `pip3 install` fails on `python-rtmidi build`. Its probably because the `libjack-dev` lib is missing. You can install it with `sudo apt-get install libjack-dev` on Debian based systems, with `brew` for MacOS, and with `pacman` for any other Arch-based system.

## Configuration and Config Tools

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

**Sardine** will be installed along with configuration tools that are meant to make configuration easy and fast. They will be **automatically** installed on your `$PATH`:
- `sardine-config` is a CLI meant to edit `config.json` from the command-line.
- `sardine-config-python` will fire `$EDITOR` to config `user_configuration.py`.
- `sardine-config-superdirt` will fire `$EDITOR` to config `default_superdirt.scd`.

Sardine will have to be runned at least once for the `config.json` file to be created.

# Using Sardine

### The internal Clock

As soon as the library is imported (`from sardine import *`), an instance of `Clock` will start to run in the background and will be referenced by the variable `c`. `Clock` is the main MIDI Clock. By default, this clock is running in `active` mode: it will send a MIDI clock signal every tick on the default MIDI port. It can also be `passive` and listen to the default MIDI port if you prefer. Don't override the `c` variable. You won't have to worry a lot about the internals. Just remember that some methods can be used and changed on-the-fly to maximize the fun you get:

* `c.bpm`: current tempo in beats per minute.
* `c.ppqn`: current [PPQN](https://en.wikipedia.org/wiki/Pulses_per_quarter_note) (Pulses per Quarter Note, used by MIDI gear).
  - be careful. The tempo might fluctuate based on the PPQN you choose. Assume that 24 is a default sane PPQN for most synthesizers/drum machines.

The Clock can either be `active` or `passive`. The `active` Clock will emit a Clock signal on the MIDI port you picked by default. The `passive` Clock will await for a MIDI Clock signal coming from elsewhere (DAWs, hardware, other softwares..). Sardine will not behave nicely if no external clock is running while in `passive` mode. Being able to send a MIDI Clock Out or to receive a MIDI Clock In is great for collaborating with other musicians. Live is also able to mirror an Ableton Link clock to a MIDI Clock.

Some interesting clock attributes can be accessed:
* `c.beat`: current clock beat since start.
* `c.tick`: current clock tick since start.
* `c.bar`: current clock bar since start (4/4 bars by default).
* `c.phase`: current phase.
* `c.accel`: `accel` for `acceleration` acts as a tempo nudge parameter. Think of it as a way to speed up or down the clock a little bit if you ever need to manually synchronise with another musician or track.

You might want to use them to compose longer pieces or just as random number generators. That's up to you!

### What does sleep really mean?

If you are already familiar with Python, you might have heard about the `sleep()` function. This function will halt the execution of a program for a given amount of time and resume  immediately after. **Sardine** does not rely on Python's `sleep` because it is *unreliable* for musical purposes! Your OS can decide to introduce a micro-delay, to resume the execution very late or even not to sleep for the duration you first indicated. 

**Sardine** proposes an alternative to regular Python sleeping backed by the clock system previously described, crafted by @thegamecracks. The `sleep()` function has been overriden to allow you to stop and resume a **swimming function** while keeping synchronization and timing accuracy.

```python
@swim
def sleeping_demo(d=1):
    print("Doing something...")
    sleep(1)
    print("Doing something else...")
    sleep(1)
    anew(sleeping_demo, d=2)

@swim
def limping(d=4):
    S('hh').out()
    sleep(3)
    S('bd').out()
    again(oversleep, d=4)
```

The **swimming function** `sleeping_demo()` will recurse after a delay of `2`. Think of the time you have in-between as spare time you can use and consume using `sleep()`. You can use that time sending instructions and composing the instructions that form your function. You can also do nothing for most of your time just like in `limping()`. You can write code in an imperative fashion, something that you might have already encountered in live coding systems such as [Sonic Pi](https://sonic-pi.net/) or **SuperCollider** `Tdefs`.

**Be careful**, you can oversleep and trigger a recursion while your function is still running, effectively overlapping versions of your **swimming functions**:   

```python
@swim
def oversleep(d=4):
    S('hh').out()
    sleep(3)
    S('bd').out()
    again(oversleep, d=0.5) # Changed the value to oversleep
```


### Temporal recursive functions

In **Sardine** parlance, a **swimming function** is a function that is scheduled to be repeated by recursion. To define a function as a **swimming function**, use the `@swim` decorator. The opposite of the `@swim` decorator is the `@die` decorator that will release a function from recursion.

```python
@swim # replace me by 'die'
def bd(d=1):
    """Loud bass drum"""
    S('bd', amp=2).out()
    anew(bd, d=1) # anew == again == cs
```

If you don't manually add the recursion to the designated **swimming function**, the function will run once and stop. Recursion must be explicit! That's another way to make a **swimming function** stop but not the recommended one!

```python
# Boring
@swim 
def bd(d=1):
    S('bd', amp=2).out()
```

The recursion can (and should) be used to update your arguments between each call of the **swimming function**. Here is an example of a very simple iterator:

```python
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

The easiest way to trigger a sound with `Sardine` is to send an OSC message to `SuperDirt`. **SuperDirt** is designed as a tool converting control messages into the appropriate SuperCollider action without having to dela with SuperCollider itself (triggering a sound, a synthesizer, tweaking a synthesis value, etc...). Most people will use the SuperDirt output instead of plugging multiple synthesizers listening to MIDI or crafting OSC listeners. The interface to SuperDirt is still very crude but fully functional. By default, **Sardine** will attempt to boot with its own `SuperCollider` and `SuperDirt` configuration. You can disable this by changing the configuration: `sardine-config --boot False`.
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
Some improvement still need to be implemented to the **SuperDirt** output to make it fully functional, such as automatically sending the current tempo in order to properly synchronise delays and other rhythmical effects.


### Composing patterns

#### Sardine grammar

Some **Sardine** objects such as `S()`, `M()` or `O()` can be patterned using a special programming language crafted for that purpose. Think of it as a glorified calculator that can also perform arithmetics on lists and with new operators such as `_`, `!` or `:`. The grammar can be found in the `ListParser.py` file if you would like to extend it and propose a new version. This allows you to write musical sequences or parametric sequences very fast and in interesting/unpredictable ways.

To test that feature, use the following functions:
* `parser(pattern: str)`: write a pattern, get the result back.
* `parser_repl()`: small REPL, similar to the Python interpeter.

Think of the pattern language as a novel way to write lists. Lists are defined as a list of operations **separated by whitespaces**. I will present some patterns in gradual order of complexity before detailing the list of available operators.

```python
# parser('1 2 3'): a list of numbers
[1.0, 2.0, 3.0]

# parser('1 2 3*3'): multiplication on last number
[1.0, 2.0, 9.0]

# parser('r+1 r/4 r*2'): random numbers and math
[1.691424279818424, 0.12130662023101241, 0.39367309061991507]

# parser('1_5 2_7'): list operators, generating lists
[1, 2, 3, 4, 5, 2, 3, 4, 5, 6, 7]

# parser('1_5/2'): you can do math on lists
[0.5, 1.0, 1.5, 2.0, 2.5]

# parser('1_5/2!!2'): and apply a transformer
[0.5, 0.5, 1.0, 1.0, 1.5, 1.5, 2.0, 2.0, 2.5, 2.5]

#  parser('1_5/2!![2,3]'): but the transformer can be a list
[0.5, 0.5, 1.0, 1.0, 1.0, 1.5, 1.5, 2.0, 2.0, 2.0, 2.5, 2.5]

#  parser('1_5/2!![2,3]|1'): because of |, it's either a long list or 1. 
[1.0]

# parser('1|2|3|4|5') # random picking
[2.0]

# parser('dada|baba|lala:2') # some operators work on names! 
['lala:1', 'lala:2', 'lala:3']
```
You get it, the pattern system can become quite complicated even if it only follows simple mathemetical rules. Here is a list of possible operators:
- math unary operators: `+2`, `-2`
- math binary operators: `+`, `-`, `*`, `/`
- `r` for a random number between `0.0` and `1.0`.
- parenthesis for complex precedence
- brackets and comma for lists
- **Sardine** binary operators:
    - `x!y`: replication, `y` times `x`.
    - `x!!y`: replication for lists, repeat `y` times each in `x`.
    - `x:y`: range, pick one between `x` and `y`.
    - `x|y`: choice. Choose one between `x` and `y`.
* **Sardine** list operators:
    - `x_y`: generate a ramp from `x` to `y`.

Try them and see if you find something interesting. Some operators might now always yield the same result depending on the result of chance based operators. Here are some patterns to get you started. I hope that they will help you to understand how all of this works:
```python
parser('1_3+(1_3|10)')
parser('r*8!4')
parser('[r,r,r]/[1,2,3]*2')
parser('1_5/2_5!!2')
```

I'm not very confident developing my own lexer/parser system. I hope to add more operators in the future. In the meantime, have fun with what is already available. Some great music can already be produced using these simple rules. 

#### Using Sardine Grammar

Every parameter available with the `S()`, `M()` or `O()` object can be patterned. The **Sardine** grammar is automatically parsed and transformed to a list when used as a parameter of these objects. Take a look at the following example:

```python
@swim
def parametrized(d=1, i=0):
    S('cp:1_10', 
        cutoff= '1_10*100',
        speed='r*2 1 2',
        legato='0.5!2 0.2 0.8', 
        room='1_10/10', 
        dry=0.2).out(i)
    again(parametrized, d=0.5, i=i+1)
```

This is a very dynamic sequence thanks to the use of the **Sardine** grammar.  There are a few things you need to know before using the **Sardine** grammar in your own patterns. Patterns are parsed automatically as lists when they are declared as strings for each parameter. By default, **Sardine** will return the first element of the list because it doesn't know what value you would like to get out of the list!

The `.out()` method can receive an optional `iter` argument (the first for convenience). This argument will indicate what value you would like to get out of the list. You can't pick a value too far in your lists and you can use asymetrical lists of different lengths. **Sardine** will round your `iter` to pick the appropriate value just like the `itertools.cycle` would have done in regular Python. Try it by yourself to understand this mechanism better:

```python
# speed=1 because first in list and no iter
S('bd', speed='1 2 3 4').out()
# speed=3 because iter=2
S('bd', speed='1 2 3 4').out(2) # change me
```

In a **swimming function**, you might use an iterator to iterate on your list by recursion:

```python
@swim
def woohoo(d=0.5, i=0):
    S('bd', speed='1_10').out(i)
    again(woohoo, d=0.125, i=i+1) # change me
```

If you wish to iterate in the opposite direction, just count in the opposite direction:

```python
@swim
def woohoo(d=0.5, i=0):
    S('bd', speed='1_10').out(i)
    again(woohoo, d=0.125, i=i-1) # change me
```

If you wish to pick a random value out of your list, but only 25% of the time, do this:

```python
from random import randint
@swim
def woohoo(d=0.5, i=0):
    S('bd', speed='1_10').out(i)
    again(woohoo, d=0.125, 
            i=randint(1,20) if random() > 0.75 else i-1)
```

Combine the iteration system with the **Sardine** grammar for maximal fun.

## MIDI

**Sardine** supports all the basic messages one can send and receive through MIDI. It will support many more in the future, including SySex and custom messages. By default, **Sardine** is always associated to a default MIDI port. It can both send and receive information from that port. If the clock is `active`, you already know that clock messages will be forwarded to all your connected softwares/gear.

You can also open arbitrary MIDI ports as long as you know their name on your system. I will not enter into the topic of finding / creating / managing virtual MIDI ports. This subject is outside the scope of what **Sardine** offers and you are on your own to deal with this. A tutorial might come in the future. 

### MIDI Out

Here is an exemple of a **swimming function** sending a constant MIDI Note:

```python
@swim
def hop(d=0.5, i=0):
    M(delay=0.3, note=60, 
            velocity=127, channel=0).out()
    anew(hop, d=0.5, i=i+1)
```

The default MIDI output is accessible through the `M()` syntax (contrary to `S`, it is not an object!). As you will see, MIDI still need some improvements to support all messages throughout the use of the same object. Note that the channel count starts at `0`, covering a range from `0` to `15`. The duration for each every note should be written in milliseconds (`ms`) because MIDI is handling MIDI Notes as two separate messages (`note_on` and `note_off`). Following the MIDI standard, note and velocity values are expressed in the range `0-127`.

Let's go further and make an arpeggio using the pattern system that will be explained later:

```python
@swim
def hop(d=0.5, i=0):
    M(delay=0.3, note='60 46 50 67', 
            velocity=127, channel=0).out(i)
    anew(hop, d=0.5, i=i+1)
```

A similar function exists for sending MIDI CC messages. Let's combine it with our arpeggio:

```python
@swim
def hop(d=0.5, i=0):
    M(delay=0.3, note='60 46 50 67', 
            velocity=127, channel=0).out(i)
    cc(channel=0, control=20, value=randint(1,127))
    anew(hop, d=0.5, i=i+1)
```

### MIDI In

MIDI INput is supported through the use of a special object, the `MidiListener` object. This object will open a connexion listening to incoming MIDI messages. There are only a few types of messages you should be able to listen to:
* MIDI Notes through the `NoteTarget` object
* MIDI CC through the `ControlTarget` object

Additionally, you can listen to incoming Clock messages (`ClockListener`) but you must generally let Sardine handle this by itself. There are currently no good reasons to do this!

Every `MidiListener` is expecting a target. You must declare one and await on it using the following syntax:

```python
a = MidiListener(target=ControlTarget(20, 0))
@swim
def pluck(d=0.25):
    S('pluck', midinote=a.get()).out()
    anew(pluck, d=0.25)
```

In this example, we are listening on CC n°20 on the first midi channel (`0`), on the default MIDI port. Sardine cannot assert the value of a given MIDI Control before it receives a first message therefore the initial value will be assumed to be `0`.

You can fine tune your listening object by tweaking the parameters:

```python
# picking a different MIDI Port
a = MidiListener('other_midi_port', target=ControlTarget(40, 4))
```

## OSC

You can send OSC (**Open Sound Control**) messages by declaring your own OSC connexion and sending custom messages. It is very easy to do so. Two methods are available depending on what you are trying to achieve.

### Manual method (not recommended)


The following example details the simplest way to send an OSC message using Sardine:

```python
from random import randint, random, chance

# Open a new OSC connexion
my_osc = OSC(ip="127.0.0.1",
        port= 23000, name="Bibu",
        ahead_amount=0.25)

# Recursive function sending OSC
@swim
def custom_osc(d=1):
    my_osc.send(c, '/coucou', [randint(1,10), randint(1,100)])
    anew(custom_osc, d=1)

# Closing and getting rid of the connexion

cr(custom_osc)

del my_osc
```

Note that you **always** need to provide the clock as the first argument of the `send()` method. It is probably better to write a dedicated function to avoid having to specify the address everytime you want to send something at a specific address:

```python
def coucou(*args): my_osc.send(c, '/coucou', list(args))
```
### Using the OSCSender object (recommended)

It is not recommended to send messages using the preceding method. You will not be able to patern parameters and addresses. Prefer the `OscSender` object, aliased to `O()`. The syntax is similar but you gain the ability to name your OSC parameters and you can use patterns to describe them (more on this later on) Compared to `S()` and `M()`, `O()` requires more parameters:
* `clock`: the clock, `c` by default.
* `OSC` object: the `OSC` connexion previously defined.

```python
# Open a new OSC connexion
my_osc = OSC(ip="127.0.0.1", port=23000, name="Bibu", ahead_amount=0.25)

# Simple address
O(c, my_osc, 'loulou', value='1 2 3 4').out()

# Composed address (_ equals /)
O(c, my_osc, 'loulou_yves', value='1 2 3 4').out()

@swim
def lezgo(d=1, i=0):
    O(c, my_osc, 'loulou_blabla', 
        value='1 2 3 4', 
        otherv='1 2|4 r*2').out(i)
    anew(lezgo, i=i+1)
```


## Crash

If you already know how to program, you know that 90% of your time is spent debugging code that doesn't work. Crashes will happen when you will play with **Sardine** but they are handled and taken care of so that the musical flow is never truly interrupted. If you write something wrong inside a **swimming function**, the following will happen: 
- if the function crashes and has never looped, it will not be recovered.
- if the function is already running and has already looped, the last valid function will be rescheduled and the current error message will be printed so that you can debug.

It means that once you start playing something, it will never stop until you want it to. You can train without the fear of crashes or weird interruptions.

## Development

**Sardine** uses [The Black Code Style](https://black.readthedocs.io/en/stable/the_black_code_style/index.html).  To enforce this code style you must run [black](https://github.com/psf/black):
```shell
black .
```