# Player arguments

Every **sender** is specialised for a task. Every **sender** will have its own special arguments. Some of them can also be aliased (*e.g* `vel` for `velocity`). Learning these arguments is part of learning the **Sardine** instrument. There is no way around it!

### MIDI Arguments

There are multiple **senders** for **MIDI** because there are different **MIDI** messages you can write. To each messsage its sender.

-   `N("pattern", velocity, channel, duration)`: the **sender** for MIDI notes.
    -   `velocity` or `vel`: how hard the note is played, from 0 to 127.
    -   `channel` or `chan`: on which channel to play the note (from 0 to 15).
    -   `duration` or `dur`: for how long to play the note (in beats).

-   `CC(control, channel, value)`: the **sender** for MIDI control changes.
    -   `control` or `ctrl`: number of the control to target (0 to 127).
    -   `channel` or `chan`: on which channel to send the control.
    -   `value` or `val`: value of that control (0 to 127).

-   `PC(program, channel)`: the **sender** for **MIDI** program changes.
    -   `program` or `prog`: program number to send.
    -   `channel` or `chan`: on which channel to send the control.

There is also a special `SY` sender that is very experimental and is used to control some very specific gear. I have currently no plan to open it for others to play but you can still send Sysex messages by using private methods of the `midi` object. The basic senders should cover 99% of your needs. If ever you were to miss one, it is easy to add them. Just contact me!


### SuperDirt Arguments

There is only one **sender** for **SuperDirt**: `D()` or `d()`. This sender is a basic interface to **SuperDirt**, allowing you to play sounds or synthesizers and to add effects to them. You will notice that the **SuperDirt** sender can take any number of arguments. It all depends on how much arguments your synthesizers can take and on how precise you want to be in the description of a specific musical event.

-   `D("pattern", orbit=0)`: the **sender** for **SuperDirt**.
    -   `orbit` : channel the sound will played on (mono or stereo).

The concept of `orbit` is just a way to precise on which channel of the audio console some specific effects should be applied. Assigning an orbit to an event guarantees that the sound you want to play (reverb amount, low-pass filter, etc&#x2026;) will only be local and not global to every other pattern currently playing. This concept of `orbit` is an important concept specific to **SuperDirt**.
