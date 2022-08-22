# IO (Input/Output)

This part of Sardine is handling input/output operations: SuperDirt (through OSC), MIDI (using the `mido` package) and OSC (using the `osc4py3` package). It also contains files dealing with user configuration (reading and writing to text and JSON files). The files can loosely be separated in two groups, from low to high level.

Low level:

- `UserConfig`: user configuration management.
- `MIDIIo`: basic MIDI connexion management.
- `Osc`: low-level OSC functionalities, used by `SuperDirtSender`.

High level:

- `MIDIListener`: MIDI Input.
- `MIDISender`: Aliased as `M()` for the default MIDI Output.
- `OSCSender`: Similar to `S()` and `M()` for OSC output.
- `SuperDirtSender`: SuperDirt interface, aliased to `S()`.

## Sender objects

Sender objects are one of the main tools you will be using while playing with **Sardine**. They are objects that compose a single message that can be sent out using the `.out(iter=0)` method. They are your main interface to the outside world (SuperCollider/SuperDirt, MIDI or OSC). These objects can receive various and/or arbitrary parameters depending on their purpose. These arguments can be *integers*, *floats* or *strings*:
- *int*/*float*: parameters used as is.
- *string* : pre-parsed using a special DSL made for writing patterns and transformed into lists.

When you import **Sardine**, `MIDISender` and `SuperDirtSender` will already be available under the name `M()` (for MIDI) and `S()` (for sound or *SuperDirt*). These objects are preconfigured objects that must be prefered to custom senders you can declare yourself (more on this later).

## SuperDirt Sender

`S()` is your main interface to *SuperDirt*, the audio engine initially programmed for **TidalCycles**. It allows you to interact with *SuperCollider*: trigger synths, audio samples or custom events programmed in *SuperCollider*. `S()` is not very complicated to grasp. The syntax is inflexible and suffers no exception.

```python
S('sound', param='1 2 3 4').out()
```

The first argument of `S()` is always a string, and must refer to a valid sound source in *SuperDirt*: synthesizer, audio sample, etc... Every other argument must be a keyword argument and should refer to a valid parameter for that sound source. In the example above, `S()` will build and send the following example to *SuperDirt*: `['sound', 'sound', 'orbit', 0.0, 'param', 1.0, 'trig', 1]`.
- `sound`: the sound you picked.
- `orbit`: the orbit, `0` if nothing is mentioned. Orbits are busses used by audio effects you can apply on sounds.
- `param`: a custom parameter, defined in your call to `S()`.
- `trig`: an internal **Sardine** parameter stating if the message is to be sent (`1`) or discarded (`0`).

The role of `S()` is to compose these messages properly and to carry them out to *SuperDirt* through OSC. As you can see, the string we feeded as the `param` argument was properly transformed into a list and its first value was used as the default value for that argument. This behavior will become clear after reading a bit about the patterning system in the global and sequences `README.md` file.

**/!\\** Don't forget the `.out()` method or you will be pretty disappointed.

## Composition and delayed messages

You can pre-declare a sound before sending it out. This allows you to build your messages incrementely before sending them out using the `.out()` method.

```python
@swim
def delayed(d=0.5):
    sound = S('bd')
    if sometimes():
        sound.shape(0.5)
    else:
        sound.speed(4)
    sound.out()
    again(delayed)
```

Do not use the assign operator (`=`). Call the attribute directly (eg: `amp()`). Any attribute can be set but they are not checked for validity. This is an useful feature if you prefer to write your code in an imperative fashion. There are other things to know about delayed composition:
- attributes can be chained: `S('cp').speed('1 2').room(0.5).out()`
- attributes **will** be parsed. You can write patterns just like you do when you send the objet out directly.

Attributes are not checked for validity. You can really write anything so be careful: spell out the *SuperDirt* attribute names correctly.

# MIDISender

The `MIDISender` object is very similar to the `SuperDirtSender` object. It is specialized in writing/sending MIDI notes. Other MIDI events are handled differently by specific methods such as `cc()`. Note that MIDI works a bit better using the default MIDI output for now because some functions need to be hard-wired to work correctly. MIDI Notes messages need a duration, a velocity, a note number and a channel:

- **duration** (`seconds`): time between a *note-on* and *note-off* event (pressing a key on an imaginary keyboard).
- **velocity** (`0-127`): think of it as the volume amplitude of a note.
- **channel** (`0-16`): the MIDI channel to send that note to on your default MIDI port.
- **note** (`0-127`): note from the lowest possible octave on a keyboard to the highest.

```python
M(delay=0.2, note=60, velocity=120, channel=0)
```

The `.out()` method is still used to carry a note out and to inform the sender of the value you would like to select in a pattern (see patterning).

# OSCSender

The `OSCSender` is the weirdest of them all. It behaves juts like the other senders but will require more work from your part. By default, the object cannot assume what OSC connexion you would like to use. For that reason, you will need to give him one as an aditional parameter. Likewise, the sender cannot assume what address you would like to send your message to. You will need to feed the object an address everytime you wish to carry a message out. There is no default OSC connexion (except for the one used by SuperDirt internally).

To use the `OSCSender` object, you will have to open manually an OSC connexion before feeding it into the object:
```python
my_osc = OSC(ip="127.0.0.1", port= 12000, name="super_connexion", ahead_amount=0.25)
O(my_osc, 'loulou', value='1 2 3 4').out()
```

Everything else works just the same.
