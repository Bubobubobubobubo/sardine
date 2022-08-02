* [ ] Allow to reset/stop the Clock (MIDI)
    * almost but not done yet.
* [ ] Receive MIDI Notes, MIDI CC and MIDI Clock
* [ ] Allow custom MIDI Out
    * opening up new connexions to other MIDI Ports
    * holding open multiple connexions
* [ ] User configuration file
    * SuperDirt parameters
    * PPQN and other clock things
    * default MIDI device (faster boot time)
    * SuperDirt real configuration
* [ ] Fix the autoboot
    * start a default session of SuperDirt
* [ ] Something fishy with the clock
    * doesn't handle stop/reset/start very well (time targets must be reset?)
    * some functions can continue to run through init even though they shouldn't
    * duplication of tasks under some conditions (how to reproduce)?
