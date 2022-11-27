import importlib
import sys
from pathlib import Path
from typing import Union, Any
from math import floor
from rich import print
from . import *
from .io.UserConfig import (
    pretty_print_configuration_file,
    read_user_configuration,
)
from .utils import config_line_printer, sardine_intro
from .sequences import PatternHolder, Player

# Reading user configuration (taken from sardine-config)
config = read_user_configuration()
clock = LinkClock if config.link_clock else InternalClock

# Printing banner and some infos about setup/config
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

# Initialisation of the FishBowl (the environment holding everything together)
bowl = FishBowl(
    clock=clock(tempo=config.bpm, bpb=config.beats),
)

# Basic handlers initialization

# MIDI Handler: matching with the MIDI port defined in the configuration file
midi = MidiHandler(port_name=config.midi)
bowl.add_handler(midi)

# OSC Handler: dummy OSC handler, mostly used for test purposes
my_osc_connexion = OSCHandler(
        ip= "127.0.0.1",
        port= 12345,
        name= "Custom OSC Connexion",
        ahead_amount= 0.0)
bowl.add_handler(my_osc_connexion)

# OSC Listener Handler: dummy OSCIn handler, used for test purposes
my_osc_listener = OSCInHandler(
        ip='127.0.0.1',
        port=33333,
        name='OSC-In test'
)
bowl.add_handler(my_osc_listener)

# SuperDirt Handler: conditionnally
if config.superdirt_handler:
    dirt = SuperDirtHandler()
    bowl.add_handler(dirt)


def swim(fn):
    """
    Swimming decorator: push a function to the clock. The function will be
    declared and followed by the clock system to recurse in time if needed.
    """
    bowl.scheduler.start_func(fn)
    return fn

def die(fn):
    """
    Swimming decorator: remove a function from the clock. The function will not
    be called again and will likely stop recursing in time.
    """
    bowl.scheduler.stop_func(fn)
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

def silence(*args) -> None:
    """
    Silence is capable of stopping one or all currently running swimming functions. The
    function will also trigger a general MIDI note_off event (all channels, all notes).
    This function will only kill events on the Sardine side. For a function capable of 
    killing synthesizers running on SuperCollider, try the more potent 'panic' function.
    """
    if len(args) == 0:
        midi.all_notes_off()
        bowl.scheduler.reset()
        return
    else:
        for arg in args:
            bowl.scheduler.stop_func(arg)

def panic(*args) -> None:
    """
    If SuperCollider/SuperDirt is booted, panic acts as a more powerful alternative to 
    silence() capable of killing synths on-the-fly. Use as a last ressource if you are
    loosing control of the system.
    """
    silence(*args)
    if config.superdirt_handler:
        D('superpanic')

def Pat(pattern: str, i: int = 0, div: int = 1, rate: int = 1) -> Any:
    """
    General purpose pattern interface. This function can be used to summon the global 
    parser stored in the fish_bowl. It is generally used to pattern outside of the 
    handler/sender system, if you are playing with custom libraries, imported code or 
    if you want to take the best of the patterning system without having to deal with
    all the built-in I/O.

    Args:
        pattern (str): A pattern to be parsed
        i (int, optional): Index for iterators. Defaults to 0.

    Returns:
        int: The ith element from the resulting pattern
    """
    parser = bowl.parser
    result = parser.parse(pattern)

    def _pattern_element(div: int, rate: int, iterator: int, pattern: list) -> Any:
        """
        Joseph Enguehard's algorithm for solving iteration speed. Used internally
        to correct the index position using a division, a rate and an iterator as 
        parameters. Allows iteration at different 'speeds' (rates) and skipping 
        some indexes!
        """
        return floor(iterator * rate / div) % len(pattern)

    return result[_pattern_element(div=div, rate=rate, iterator=i, pattern=result)]

class Delay:
    """
    Delay is a compound statement providing an alternative syntax to the overridden 
    sleep() method. It implements the bare minimum to reproduce sleep behavior using
    extra indentation for marking visually where sleep takes effect.
    """

    def __init__(self, duration: Union[int, float] = 1, delayFirst: bool = True):
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

_surfing_patterns = PatternHolder(
    midi_handler=midi,
    superdirt_handler=dirt if config.superdirt_handler else None,
    osc_handler=None,  #TODO: reimplement
)
bowl.add_handler(_surfing_patterns)

# TODO: Rewrite surfing methods
#
# Surfing methods provide an alternative syntax for Sardine that emulates FoxDot. It is
# generally easier for live coders to start using Sardine with this technique, as it is
# closer to what they expect from a live coding interface.

# for (key, value) in __surfing_patterns._patterns.items():
#     globals()[key] = value
# swim(__surfing_patterns._global_runner)
# surf = __surfing_patterns
# play, play_midi, play_osc, run = (
#         Player.play, 
#         Player.play_midi, 
#         Player.play_osc,
#         Player.run
# )

# Aliases!

again = bowl.scheduler.start_func
sleep = bowl.sleep

I, V = bowl.iterators, bowl.variables  # Iterators and Variables from env
P = Pat                                # Generic pattern interface
N = midi.send                          # For sending MIDI Notes
PC = midi.send_program                 # For MIDI Program changes
CC = midi.send_control                 # For MIDI Control Change messages
Ocustom = my_osc_connexion.send

if config.superdirt_handler:
    SC = dirt._superdirt_process
    D = dirt.send

# Clock start
bowl.start()
