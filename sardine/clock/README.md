# Clock Mechanism

The Clock mechanism is the heart of **Sardine**. It is based on the `asyncio` library and the new asyncio REPL (Python 3.8+). Many thanks to @thegamecracks for his invaluable help on this feature! The Clock mechanism is divided in two core components:
- `Clock`: a basic MIDI Clock that can either run in `active` or `passive` mode.
- `AsyncRunner`: a complex system of hot-reloadable asynchronous functions aware of tempo/time.

## Clock

By design, **Sardine** is thought as a tool meant to be synchronized with other MIDI clock-dependant or clock-emitting devices. The Clock needs a default `midi_port` that can either be a physical MIDI port or a virtual one. The clock needs a `ppqn` (pulses per quarter note), the shortest possible time division it can work with, and a global tempo (`bpm`). You can either choose the default MIDI port when importing **Sardine** or set a default one using `sardine-config` (see **configuration**).

As soon as **Sardine** is imported in the global scope, a default `Clock` will start to run. It can be accessed using the `c` variable. Be careful not to override it. You can introspect the current state of the clock using clock attributes or using the very verbose `debug` mode.

After running `c.debug = True`:
```python 
...
BPM: 130.0, PHASE: 15, DELTA: 0.001726 || TICK: 495 BAR:2 3/4
BPM: 130.0, PHASE: 16, DELTA: 0.001729 || TICK: 496 BAR:2 3/4
BPM: 130.0, PHASE: 17, DELTA: 0.001475 || TICK: 497 BAR:2 3/4
BPM: 130.0, PHASE: 18, DELTA: 0.000634 || TICK: 498 BAR:2 3/4
BPM: 130.0, PHASE: 19, DELTA: 0.000614 || TICK: 499 BAR:2 3/4
BPM: 130.0, PHASE: 20, DELTA: 0.001333 || TICK: 500 BAR:2 3/4
...
```

The clock can either be `active` or `passive`:
- `active`: actively emit MIDI clock ticks on the default MIDI output.
- `passive`: awaiting a MIDI tick coming from the default MIDI input.

You can fine tune the granularity of time by tweaking the `c.ppqn` attribute. Most MIDI capable drum machines and synthesizers are running at `24` ppqn but some will need a different value. `c.bpm`, `c.ppqn`, `c.tick`, `c.bar`, `c.phase` are valid clock attributes you can use in your **Sardine** code if you ever need to.

The clock can be manually pushed forward or backwards using the `accel` parameter (very similar to a jog wheel on a regular DJ controller). The `accel` (`0.0` by default) can be set between `0` (normal speed) to `100` (double speed). This feature was thought as a way to synchronise with other devices that are not capable of listening to a MIDI clock signal.

Generally speaking, you don't need to interact with the MIDI clock at all if ever to set the tempo/ppqn and the `accel` parameter. 

# AsyncRunner

**Sardine** makes use of a special type of function called **swimming functions**. They are derivatives of `async` functions but are introducing some novel features: hot-reloadable, time-aware, error/crash proof, etc... These functions are the basic object you are manipulating while playing with Sardine. Before diving deeper, here is a short description of some features introduced by **swimming functions**:

- they are hot-swappable/reloadable: you can override/tweak/rewrite a function at runtime, while the code is already running.
- they can't/won't crash: if you ever write an incorrect function, it will crash but an older and valid version of your function will be invoked while you fix your current code. The musical flow will not be interrupted.
- they are thought to be recursive functions: a **swimming function** is a recursive function that will reschedule itself later in time, just not immediately like a regular recursive function. 

## A basic example

**Swimming functions** need a `delay` parameter, named `d`. By default, `d` is assumed to be `1`, so you don't need to specify it directly in the signature every time. Take a look at this minimal working example of a swimming function:

```python
@swim
def hey():
    print("Hey!")
    again(hey)
```

The `@swim` decorator will take the function and use it to create an `AsyncRunner`. `@swim` is an alias to `clock.schedule(func)`, itself alised multiple times for conveniance and readability: `cs`, `again`, `anew`, etc... All these names refer to the same public method of the default `Clock` instance. Note that even in the minimal example, `clock.schedule` is called twice: once for creating an `AsyncRunner`, another time to carry over arguments for the next call, later in time.

`clock.schedule -- starts --> func --> clock.schedule(func, **kwargs)` 

Removing the last call to `clock.schedule` will effectively halt the recursion and stop your **swimming function**. Note that you can also use the `@die` decorator to do the same without having to comment out a line and while keeping everything readable and easy for the eye.

Just like mentioned earlier concerning the `Clock`, you don't have/need to deal with `AsyncRunners` directly. This mechanism is entirely internal and must be handled by the `@swim`, `@die` and aliases to `clock.schedule` (`cs`, `again`, `anew`). 

## Using arguments

**Swimming functions** can carry over keyword arguments. That way, **swimming functions** can have their own local state without having to rely on global state excessively. You can add and remove keyword arguments as much as you like but make sure to remove them on both sides if needed. Otherwise, you might end up with a crash. Handling local state using keyword arguments is extremely valuable for crafting iterators and to play with data:

```python
from random import choice, randint
@swim
def data_fun(d=0.5, i=0, i2=0):
    S('cp', speed=i2/2).out(i)
    again(
        data_fun, d=0.5/choice([2,0.5]), 
        i=i+1, i2=randint(1,40))
```

There is no golden rule about the usage of global state but I would recommend to use it to store important information shared by many **swimming functions**: OSC connexions, global values, regular Python iterators (such as the very fun `itertools.cycle`) etc...