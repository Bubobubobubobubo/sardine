import asyncio
import importlib
import os
import sys
from pathlib import Path
from sys import argv
from typing import Union, Callable, Any
from math import floor

from rich import print
from rich.panel import Panel

from . import *
from .io.UserConfig import (
    pretty_print_configuration_file,
    read_user_configuration,
)
from .utils import config_line_printer, sardine_intro
from .sequences import PatternHolder, Player

config = read_user_configuration()

# | INITIALISATION |#
CRASH_TEST = False

# Reading user configuration
config = read_user_configuration()

print(sardine_intro)
print(config_line_printer(config))

# Load user config
if Path(f"{config.user_config_path}").is_file():
    spec = importlib.util.spec_from_file_location(
        "user_configuration", config.user_config_path
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    from user_configuration import *
else:
    print(f"[red]No user provided configuration file found...")

# Real initialisation takes place here ############################
clock = LinkClock if config.link_clock else InternalClock
# clock = LinkClock if config.link_clock else InternalClock
bowl = FishBowl(
    clock=clock(tempo=config.bpm, bpb=config.beats),
)
# Attaching handlers
midi = MidiHandler()
bowl.add_handler(midi)

if config.superdirt_handler:
    dirt = SuperDirtHandler()
    D = dirt.send
    bowl.add_handler(dirt)

# Starting the clock
bowl.start()


def swim(fn):
    """
    Swimming decorator: push a function to the clock. The function will be
    declared and followed by the clock system to recurse in time if needed.
    """
    bowl.scheduler.schedule_func(fn)
    return fn


def sleep(n_beats: Union[int, float]):
    """Artificially sleep in the current function for `n_beats`.

    Example usage: ::

        @swim
        def func(delay=4):
            sleep(3)
            for _ in range(3):
                S('909').out()
                sleep(1/2)
            again(func)

    This should *only* be called inside swimming functions.
    Unusual behaviour may occur if sleeping is done globally.

    Using in asynchronous functions
    -------------------------------

    This can be used in `async def` functions and does *not* need to be awaited.

    Sounds scheduled in asynchronous functions will be influenced by
    real time passing. For example, if you sleep for 500ms (based on tempo)
    and await a function that takes 100ms to complete, any sounds sent
    afterwards will occur 600ms from when the function was called.

    ::

        @swim
        async def func(delay=4):
            print(bowl.clock.time)  # 0.0s

            sleep(1)     # virtual +500ms (assuming bowl.clock.tempo = 120)
            await abc()  # real +100ms

            S('bd').out()           # occurs 500ms from now
            print(bowl.clock.time)  # 0.6s
            again(func)

    Technical Details
    -----------------

    Unlike `time.sleep(n)`, this function does not actually block
    the function from running. Instead, it temporarily affects the
    value of `BaseClock.time` and extends the perceived time of methods
    using that property, like `SleepHandler.wait_after()`
    and `BaseClock.get_beat_time()`.

    In essence, this maintains the precision of sound scheduling
    without requiring the use of declarative syntax like
    `S('909', at=1/2).out()`.

    """
    duration = bowl.clock.get_beat_time(n_beats, sync=False)
    bowl.time.shift += duration


def die(fn):
    """
    Swimming decorator: remove a function from the clock. The function will not
    be called again and will likely stop recursing in time.
    """
    bowl.scheduler.remove(fn)
    return fn

def silence(*args) -> None:
    """Silence a function of every function currently running"""
    if len(args) == 0:
        midi.all_notes_off()
        bowl.scheduler.reset()
        return
    else:
        for arg in args:
            bowl.scheduler.remove(arg)

def Pat(pattern: str, i: int = 0, div: int = 1, rate: int = 1) -> Any:
    """Generates a pattern

    Args:
        pattern (str): A pattern to be parsed
        i (int, optional): Index for iterators. Defaults to 0.

    Returns:
        int: The ith element from the resulting pattern
    """
    parser = bowl.parser
    result = parser.parse(pattern)

    def _pattern_element(div: int, rate: int, iterator: int, pattern: list) -> Any:
        """Joseph Enguehard's algorithm for solving iteration speed"""
        return floor(iterator * rate / div) % len(pattern)

    return result[_pattern_element(div=div, rate=rate, iterator=i, pattern=result)]

class Delay:
    """
    with delay(0.5):
        do_stuff()
    """

    def __init__(self, duration: Union[int, float] = 1, delayFirst: bool = True):
        """
        This compound statements needs to know two things, already provided
        by some default values:
        duration: for how long do we wait before or after the block?
        delayFirst: are we waiting before or after the block?
        """
        self.duration = duration
        self.delayFirst = delayFirst

    def __call__(self, duration=1, delayFirst=False):
        self.duration = duration
        self.delayFirst = delayFirst
        return self

    def __enter__(self):
        if self.delayFirst:
            sleep(self.duration)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.delayFirst:
            sleep(self.duration)

__surfing_patterns = PatternHolder(
    clock=bowl.clock, 
    MIDISender=midi, 
    SuperDirtSender=dirt if config.superdirt_handler else None,
    OSCSender=None #TODO: reimplement
)

for (key, value) in __surfing_patterns._patterns.items():
    globals()[key] = value
swim(__surfing_patterns._global_runner)
surf = __surfing_patterns
play, play_midi, play_osc, run = (
        Player.play, 
        Player.play_midi, 
        Player.play_osc,
        Player.run
)



# Aliases!

again = bowl.scheduler.schedule_func
sleep = bowl.sleep
I, V = bowl.iterators, bowl.variables
P = Pat
M = midi.send
# CC = midi.send_control
if config.superdirt_handler:
    SC = dirt._superdirt_process
    D = dirt.send
