## I - Modes

Nothing would be happening without the **Sardine** clock. The clock is the central piece of the library. It is always running in the background and it manages function execution, recursion and timing. This is a complex and fragile mechanism. **Python** is particularly bad when you are trying to enforce timing guarantees. The **clock** is still a work in progress. If you are good at programming clocks or similar mechanisms, please come have a chat with me :)

The clock works pretty well until the moment it doesn't work anymore. If you are trying to be extra precise, follow these instructions:

- kill every other non-essential program or process. We are trying to minimise context switching between the **Sardine** clock mechanism and the outside world.

- start **Sardine** with `sudo` or administrator priviledges. This allows me to `nice` the process a fair bit. **Sardine** will have a higher priority among other processes.

- be gentle, don't try to go faster than time. There is a minimal time division that the clock can handle. You can find out about it by typing `c._get_tick_duration()` a few times to see what the minimal amount of time between recursions is at your given tempo.


Internally, the **Clock** instance, aliased as `c`, is managing a lot of things. It is involved in proper message handling, ensuring time guarantees and much more.

### A) MIDI Mode

#### a) Active

By default, the clock is running in **active mode**. It means that **Sardine** will emit a MIDI Clock signal on the default MIDI port. A MIDI Clock works by `ticking` constantly and it usually relies on a *pulses per quarter note* division, that indicates how many pulses form a basic rhythmic division. Hardware equipment are usually working at 24 or 48 PPQN but you can go much higher. **Sardine** tries to work well at these values, but the rest is really grey area. You are on your own.

#### b) Passive

In passive mode, **Sardine** will await for a clock signal. If the signal never comes, nothing will happen and you will be stuck in time. Please make sure to have a steady clock signal before booting **Sardine**. This mode is experimental and has never been truly tested.

### B) Link Mode

**Sardine** can synchronise with other audio software / equipment through the Ableton Link protocol. You can switch from the regular clock to the **Link** clock by running the `c.link()` or `c.unlink()` method. Note that it is better to do this at startup and to shut down every running pattern before doing so because **Sardine** will dramatically jump in time. Some of your patterns might lie somewhere in the future, or somewhere in the past.

This synchronisation mode works reasonably well. **Sardine** has been tested live on stage multiple times with the **Link** synchronisation enabled and it was stable enough to run for several hours unmonitored :) Depending on your hardware, you might have to nudge some messages in time a fair bit but it has nothing to do with the synchronisation itself but more likely with how your system is handling messages (internal delay of some sort).

### Log information

For your own curiosity, you can turn on clock monitoring by switching a boolean: `c.debug = True`. Be careful, the information is very invasive and it can be very fast. You will see how the clock advances in time by ticking at a steady rate. Please turn this mode off before playing anything because printing is not innocent, it can have a temporal cost that will cause the clock to slow down a little.

## II - Attributes and useful information

- `c.beat`: current beat.
- `c.phase`: current phase.
- `c.ppqn`: current pulses per quarter note.
- `c.tick`: current tick.

## III - Shifting / Latency 

- `c._superdirt_nudge`: adding a delay the timestamp attached to each **SuperDirt** message.
- `c._midi_nudge`: nudging MIDI in time.
- `c.accel`: acceleration of the clock, between `0` and `100`%. Similar to a jog on a DJ controller.
- `c.nudge`: nudging clock temporarily (for one cycle).