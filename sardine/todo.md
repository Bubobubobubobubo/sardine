* [ ] Clock Related:
    * Allow to reset/stop the Clock (MIDI)
    * adding an offset to function start (argument?)
    * small delay when restoring a function
    * accel can go higher than 100?
    * high-delta resulting in negative tick duration corner case.
    * fix phase never being reset
* [ ] MIDI related:
    * Receive MIDI Notes, MIDI CC and MIDI Clock
    * opening up new connexions to other MIDI Ports
    * holding open multiple connexions
    * repair MIDI so that MIDI notes can be sent.
* [ ] User configuration file
    * SuperDirt configuration
* [ ] Fix the autoboot
    * boot, hold and manage a SuperCollider process.
    * stdin / stdout / stderr streams
    * API from Sardine to SuperCollider / SuperDirt
* [ ] SuperDirt related
    * how should bpm be communicated to SuperDirt?
        * delay/delayfeedback/etc.. can't work without it.
