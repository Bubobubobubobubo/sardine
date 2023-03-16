# The FishBowl

The `FishBowl` is central to the **Sardine** system. As its name might suggest, it is what holds everything together. Properly speaking, it is the environment, the water, what makes the fishes swim :) The system is composed of some **hard dependencies** and many **soft dependencies**. **Hard dependencies** are important components like the **clock** or the **parser**. They are needed all the time. As such, you can&rsquo;t really remove them or everything would fall apart. **Soft dependencies** are the various **senders** or I/O components that you use to perform your music. Some of them are installed based on the content of your configuration, some can be created on the fly later on.

### Hard dependencies

Core components cannot be removed from the `FishBowl`. However, they can be swapped! It means that you can all of the sudden rip off the current **clock** and switch to a new one. The system might hiccup a bit but it will recover! To do so, note that you can use two important methods:

- `bowl.swap_clock(clock: "BaseClock")`: swaps a clock. `InternalClock()` and `LinkClock()` are the two clocks currently implemented. The latter is used for synchronisation with every device capable of using the Ableton Link protocol.
- `bowl.swap_parser(parser: "BaseParser")`: switch from a parser to another parser. There is no reason to do that because there is only one parser for the moment but it might be useful in the future.


### Soft dependencies

This is where the fun begins. Pretty much everything in the **Sardine** system is a modular component that can be added or removed. Take a look at the `run.py` file if you want to see how the system is first initialized. By default, Sardine is proposing a small collection of **handlers** / **senders** that will allow you to send or receive **MIDI**, **OSC** or **SuperDirt** messages. Some other handlers are used for various internal functions that you might not care about. Take a look at the following code detailing how to add modular components:

```python 
# Adding a MIDI Out handler: sending MIDI notes
# control changes, program changes, etc...
midi = MidiHandler(port_name=str(config.midi)) # new instance of the Handler
bowl.add_handler(midi) # adding the handler to the FishBowl

# OSC Loop: internal component used for handling OSC messages
osc_loop = OSCLoop() # new instance of the Handler
bowl.add_handler(osc_loop)  # adding the handler to the FishBowl

# OSC Handler: dummy OSC handler
dummy_osc = OSCHandler(
    ip="127.0.0.1",
    port=12345,
    name="My OSC sender",
    ahead_amount=0.0,
    loop=osc_loop,
)

# Aliasing some methods from the handlers for later :)
M = midi.send
CC = midi.send_control_changes
PC = midi.send_program_changes
O = dummy_osc.send
```

Please take note of the `bowl.add_handler method`. If you don't add your component to the `FishBowl`, your component will inevitably crash!
This is a fairly common mistake, especially if you are working in a hurry.

### Messaging system

You might wonder what the `FishBowl` is actually doing behind the scene. Factually, it allows component to talk with each other by sharing a reference to the bowl. It means that any component can send a message to any other component. It also means that this same component can promptly react to any event dispatched through the `FishBowl`. Internal messages are sent using the `bowl.dispatch(message_type: str, *args)` method. This is how messages such as `bowl.('pause')`, `bowl.('resume')`, `bowl.('stop')` and `bowl.('play')` are able to stop and resume everything when needed. They are messages dispatched to the `FishBowl` making everyone aware that a major event occured.

- Introduction to the concept.
- Hard dependencies
- Soft dependencies
- Messaging system.


