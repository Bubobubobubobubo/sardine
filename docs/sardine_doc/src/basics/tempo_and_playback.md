# Tempo and playback

Sardine executes code based on timing given by its clock. The clock starts with Sardine and runs until Sardine exits. There are two clocks:

-   **internal clock:** Your regular system clock.
-   **external clock:** A special clock **for synchronisation on the network**. (See Diving Deeper)

Clock commands:

-   `clock.tempo` reports the current tempo in bpm.
-   `clock.tempo = 140` sets tempo to 140 bpm.

Position in time:

-   `clock.phase` Position in phase (0.0 - 1.0).
-   `clock.beat` Cumulative number of beats (note: doesn&rsquo;t reset at each bar.)
-   `clock.bar` Cumulative number of bars.
-   `clock.time` time elapsed since start in seconds (monotonic time)
-   `clock` shows elapsed time, tempo, beats per bar

Bowl commands can be used to start/stop the clock, which will also impact any Player output.

-   `bowl.pause()` / `bowl.resume()` : pause and resume runnnig code and stops/resumes the clock.
-   `bowl.stop()` / `bowl.start()`: stop and play. (Start does not restart the clock.)
