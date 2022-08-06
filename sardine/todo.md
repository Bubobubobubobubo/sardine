* [ ] Clock Related:
    * Allow to reset/stop the Clock (MIDI)
    * adding an offset to function start (argument?)
    * accel can go higher than 100?
    * high-delta resulting in negative tick duration corner case.

* [ ] MIDI related:
    * MIDI In
        * Check if MidiListener is correct
        * Receive MIDI Notes, MIDI CC and MIDI Clock
        * Open new arbitrary connexions
    * MIDI Out
        * Hold open multiple connexions
        * Midi Note and Midi CC through scheduling mechanism
        * Support whole range of basic MIDI messages (program change, etc..)

* [ ] SuperDirt related
    * how should bpm be communicated to SuperDirt?
        * delay/delayfeedback/etc.. can't work without it.
