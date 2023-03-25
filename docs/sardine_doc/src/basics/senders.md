# Senders

Senders are required building blocks used in all ways of making sound with Sardine. 

`d('bd')` is a **Sender**. It is a special function that sends messages to musical applications and audio tools. It also provides an interface to the pattern languages (**Sardine**, **Ziffers**). Basically, **senders provide a gate outside of Sardine**.

### Default Senders

The *Case* signifies whether the sender is used in a **Player** (*lower*), or **@swim** function (*UPPER*). See [Player vs @swim](player-vs-swimfunction.md). Using the [Ziffers pattern language](../pattern_languages/ziffers.md) requires different senders. 

| Player  | @swim   | Purpose and description   |
|:-------:|:-------:|:----------|
| **Sardine** | **Senders**       | senders used with Sardine patterns  |
| d( )   | D( )  | **SuperDirt** - samples and synthesizers |
| n( )   | N( )  | **MIDI** notes |
| cc( )  | CC( ) | **MIDI** control messages |
| pc( )  | PC( ) | **MIDI** program changes |
| sy( )  | SY( ) | **MIDI** sysex message |
| **Ziffers** | **Senders**       | senders used with Ziffers patterns  |
| zd( )  | ZD()  | **Ziffers SuperDirt** - samples /synths with Ziffers patterns|
| zn( )  | ZN()  | **Ziffers MIDI** notes with Ziffers patterns |

There is also a standalone `zplay()` sender associated with **Ziffers** documented in the [Ziffers](../pattern_languages/ziffers.md) section.

### Arguments and syntax

Senders require arguments and keyword arguments. These provide the values that represent notes, samples, patterns, parameters, etc. Here are the syntax rules:

- Patterns are given as strings with double or single quote. No comma is tolerated in the pattern.
  - Using `d('bd, cp')` will error. There are some exceptions to the comma rule, covered in the Pattern Language section.
- Patterns use a distinct syntax from **Python**. Learn about it in the [Pattern Languages](../pattern_languages.md) section.
- Keyword parameters are regular keyword arguments: `parameter=value`. Arguments are separated with commas!

#### Sender example with arguments

```python
## Sender syntax: This statement evaluates correctly but will not produce any sound.
d('bd cp', speed='1 2', shape=0.5, p='0.5!4 0.25!2') # sender syntax

## It needs to be called from a Player:
Pa * d('bd cp', speed='1 2', shape=0.5, p='0.5!4 0.25!2') 
```

- `'bd cp'`: initial argument to SuperDirt. Specifies the pattern of samples and synthesizers.
- `speed='1 2'`: speed is a SuperDirt sampling parameter, set here with a pattern that alternates between 1 and 2 (doubles speed = raise pitch an octave).
- `shape=0.5`: shape is an effects parameter from SuperDirt, single value. 
- `p='0.5!4 0.25!2'`: the letter "p" is shorthand for "period". It is set to a more complex pattern that controls the playback rhythm. 

#### More sender examples

Here are some additional patterns using the **Sardine senders**. If your patterns are getting longer, you can indent them on multiple lines.
This is just normal Python code after all!

```python
Pa * n('C5 E5 G5', p=0.25) # playing a chord, one note every 1/4 of a beat.
Pb * cc(ctrl=20, chan=0, value='rand*127') # sending a random MIDI control on ctrl 20, channel 0
Pc * d('tabla tabla:2') # Playing audio samples of an indian tabla
```

