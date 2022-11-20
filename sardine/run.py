import asyncio
import importlib
import os
import sys
from pathlib import Path
from sys import argv

from rich import print
from rich.panel import Panel

from . import *
from .io.UserConfig import (
    pretty_print_configuration_file,
    read_user_configuration,
)
from .utils.Messages import config_line_printer, sardine_intro

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
bowl.add_handler(MidiHandler())
if config.superdirt_handler:
    dirt = SuperDirtHandler()
    bowl.add_handler(dirt)

# Adding a parser (I guess?)
# bowl.swap_parser(ListParser)

# Starting the clock
bowl.start()


def swim(fn):
    """
    Swimming decorator: push a function to the clock. The function will be
    declared and followed by the clock system to recurse in time if needed.
    """
    bowl.scheduler.schedule_func(fn)
    return fn



def swim(fn):
    """
    Swimming decorator: push a function to the clock. The function will be
    declared and followed by the clock system to recurse in time if needed.
    """
    bowl.scheduler.schedule_func(fn)
    return fn

def die(fn):
    """
    Swimming decorator: remove a function from the clock. The function will not
    be called again and will likely stop recursing in time.
    """
    bowl.scheduler.remove(fn)
    return fn

# Aliases!

again = bowl.scheduler.schedule_func
sleep = bowl.sleep

if CRASH_TEST:

    # Re-establishing Sardine Syntax to the V1 counterpart, making it better when possible
    @swim
    def dummy_swimming_function(d=0.5, i=0):
        D('bd')( 1,1,1)
        a(dummy_swimming_function, d=0.5, i=i+1)


    Pa >> play('bd')
    Pb >> play_midi('60,67')
    Pc >> play_osc('/hello/surf/', value=1, other=2, otherother=3)
