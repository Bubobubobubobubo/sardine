* [ ] Clock Related:
    * Allow to reset/stop the Clock (MIDI)
    * adding an offset to function start (argument?)
    * accel can go higher than 100?
    * high-delta resulting in negative tick duration corner case.
* [ ] MIDI related:
    * MIDI Out
        * Hold open multiple connexions with simple API
* [ ] SuperDirt related
    * how should bpm be communicated to SuperDirt?
        * delay/delayfeedback/etc.. can't work without it.
* [ ] Configuration related
    * Make `__init__.py` more configurable
        * autoboot, no-autoboot
        * passive clock/active clock
        * running or importing user-made code
