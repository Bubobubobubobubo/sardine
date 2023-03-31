# MIDI Controller

You can use `MIDIController` to create a new sender that will allow
you to send multiple MIDI control messages at the same time, much 
alike a regular MIDI controller. This feature is very similar to the
[MIDIInstrument](midi_instrument.md) approach described earlier. 
This is an interesting approach for hardware or external software
base approaches to playing Sardine:
- you can name every control change you are using instead of relying on numbers and variable names.
- you only have one interface to control multiple related messages.
- you can build yourself a library of MIDI controllers so that you don't have to do it again.

To create a new `MIDIController`, you will need two things:
- a mapping describing the MIDI configuration of your controller.
- a call to `MIDIController` to create both the **sender** and 
  the **player** for your controller.

```python
cmap = {
    'reverb': {'channel': 0, 'control': 20},
    'delay': {'channel': 0, 'control': 21},
}
```

Note that we provide both a **channel** and a **control number** for the CC we want to map.
Once this is done, you can call the `MIDIController` function to create your new instrument.
Please note that we are capturing two new names. By convention, the uppercase version is for
**senders** while the lowercase version is for **players**.

```python
Controller, controller = MIDIController(midi, channel=0, controller_map=cmap)
```
You can now use this new MIDI controller in each of the playing modes:

You can now use it:
```python
Pa * controller(reverb='rand*120', delay='rand*120')
```
