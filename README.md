# Sardine

Sardine is a small fun summer project made using asyncio and the [mido MIDI Library](https://github.com/mido/mido). It is an attempt to get a small MIDI Clock and MIDI scheduling library ready for sequencing synthesizers and hardware drum machines on-the-fly. For the time being, I will try to support the whole range of MIDI messages before trying to branch out using OSC.

## Installation

Installation is pretty simple:
1) run `setup.py` using `pip3 install -e .` to download required libraries and install the library.
2) open a new interactive session using `python3 -m asyncio`
   - **/!\\ Make sure that you are running the asyncio REPL!**
3) import the library `from sardine import *`
4) Follow the prompt to connect to a MIDI Output.

## Usage

As soon as the library is imported, an instance of `Clock` will start to run in the background and will be referenced to by the variable `c` (in lowercase). `Clock` is the main MIDI Clock you will be playing with. Because the project is still very experimental and things move often, you won't have to worry a lot about the internals. Just remember that some methods could be useful:
* `c.bpm`: current BPM (can be inexact depending on your `ppqn`)
* `c.ppqn`: current [PPQN](https://en.wikipedia.org/wiki/Pulses_per_quarter_note) (1-??).
  - be careful. The tempo might fluctuate based on the PPQN you choose.
* `c.get_tick_duration`: duration of a clock tick.

This library is unusable as of now without knowing the internals. I don't recommand using it before a proper release.
