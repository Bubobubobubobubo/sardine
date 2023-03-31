# External Clock

Sardine lets you chose between two clocks: the `InternalClock` and the `LinkClock`:

-   the `InternalClock` is a monotonic clock tied to your system time. It is the default time used by your system.
-   the `LinkClock` is an interface to the [Ableton Link](https://www.ableton.com/en/link/) link protocol.

You can use `sardine-config` to change which clock your **Sardine** is using.

Because clocks share the same interface, there is no visible difference to using one VS the other. However, only the `LinkClock` will allow proper synchronisation with outside peers.

To synchronise, you simply need to share a local network with any other application (or **Sardine** instance) using the Ableton Link protocol. If nothing is blocking the signal (firewall, network protection), your **Sardine** will automatically try to match with the tempo of all the other applications around.
The tempo given by Ableton Link is an average tempo that adjusts itself according to the tempo given by everyone. There is no master instance and no passive instance that just listens like MIDI. This means that anyone can submit a tempo change, and that this change will apply to all players.

Internally, the Link clock is implemented differently. In order for it to work with Sardine, a task is started in the background. This task will regularly (several times per second) fetch new information about the temporal position of the clock and propagate this information to all Sardine components that need it.


