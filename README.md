# Sardine

Sardine is a small fun summer project made using asyncio and the [mido MIDI Library](https://github.com/mido/mido). It is an attempt to get a small MIDI Clock and MIDI scheduling library ready for sequencing synthesizers and hardware drum machines on-the-fly. For the time being, I will try to support the whole range of MIDI messages before trying to branch out using OSC.

## Installation

Installation is pretty simple:
1) run `setup.py` using `pip3 install -e .` to download required libraries and install the library.
2) open a new interactive session using `python3 -m asyncio`
   - **/!\\ Make sure that you are running the asyncio REPL!**
3) import the library `from bibu import *`

## Usage

This library is unusable as of now without knowing the internals. I don't recommand using it before a proper release.
