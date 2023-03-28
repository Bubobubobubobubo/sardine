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

### Tempo change
Tempo changes can be achieved in @swim by using the Pattern Object on the `clock.tempo` value. For details on the Pattern Object, see [Diving Deeper > Patterning everything](../diving_deeper/patterning_everything.md).

In the first function below, the Pattern Object uses the ramp operator to increment the tempo by 2 BPM between 90 and 180, then hold the tempo, and then decrease back faster to 90 (decrements by 4 BPM). To see the tempo values print out, uncomment the print line. 
- Pattern changes will come at the rate set by the function's period value. Setting the period to 1 (`p=1`) will make changes happen every beat. Set a higher value for more gradual tempo changes.
- It is best to have a separate function just for clock.tempo changes. That keeps the clock patterns independant from musical functions. 
- **Tips**
    - Set the clock.tempo to your initial value every time you run the function. When you reload the function the clock will be at it's last value.
    - Reset your clock to your default when you are done!

```python
# @swim to manage clock.tempo changes
# tempo increases from 90 -> 180, holds there, then decreases back to 90

clock.tempo=90
@swim
def clockPat(p=1, i=0):
    #print(f"clock.tempo: ", clock.tempo)
    clock.tempo=P('[90:180,2] [180:181,0.1] [180:90,4]', i)
    again(clockPat, p=1, i=i+1)

@swim
def hh(p=1, i=0):
    D('hh27:2 hh27:9 hh27:1', i=i)
    D('hh:4 . hh:9', i=i) 
    again(hh, p=0.5, i=i+1)

# reset your clock value when you are done!
clock.tempo=120
```