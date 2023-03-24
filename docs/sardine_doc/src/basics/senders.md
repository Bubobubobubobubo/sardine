# Senders

Senders are required building blocks used in all ways of making sound with Sardine. 

`d(bd)` is a **Sender**. It is a special function that sends messages to musical applications and audio tools. It also provides an interface to the pattern languages (Sardine, Ziffers). Basically, **senders provide a gate to the outside world**.

## Default Senders

The *Case* signifies whether the sender is used in a Player (lower), or @swim function (UPPER). Using the Ziffers pattern language requires different senders. 

| Player  | @swim   | purpose   |
|:-------:|:-------:|:----------|
| d('')   | D('')  | **SuperDirt** - samples and synthesizers |
| n('')   | N('')  | **MIDI** notes |
| cc('')  | CC('') | **MIDI** control messages |
| pc('')  | PC('') | **MIDI** program changes |
| Ziffers |        | senders used with Ziffers patterns  |
| zd('')  | ZD('')  | **Ziffers SuperDirt** - samples /synths with Ziffers patterns|
| zn('')  | ZN('')  | **Ziffers MIDI** notes with Ziffers patterns |

## Arguments and syntax

Senders require arguments. These provide the values that represent notes, samples, patterns, parameters, etc. Syntax rules:
- patterns in single quotes 
  - No comma within pattern: `'bd, cp'` will error (There are some exceptions to the comma rule, covered in the Pattern Language section.)
- parameter=value
- arguments separated by comma

Sender with arguments:
```python
## Sender syntax: This statement evaluates but will not produce any sound.
d('bd cp', speed='1 2', shape=0.5, p='0.5!4 0.25!2') # sender syntax

## It needs to be called from a Player:
Pa >> d('bd cp', speed='1 2', shape=0.5, p='0.5!4 0.25!2') 
```

- `'bd cp'`: initial argument to SuperDirt. Specifies the pattern or sequence of samples and synthesizers.
- `speed='1 2'`: speed is a SuperDirt sampling parameter, set here with a pattern
- `shape=0.5`: shape is an effects parameter from SuperDirt, single value. 
- `p='0.5!4 0.25!2'`: the letter p is shorthand for "period". It is set to a more complex pattern. 

## More sender examples
TBD: add ziffers example

```python
Pa >> n('C5 E5 G5', p=0.25) # playing a chord, one note every 1/4 of a beat.
Pb >> cc(ctrl=20, chan=0, value='rand*127') # sending a random MIDI control on ctrl 20, channel 0
Pc >> d('tabla tabla:2') # Playing audio samples of an indian tabla
```

