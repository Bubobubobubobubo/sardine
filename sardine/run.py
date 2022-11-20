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
bowl = FishBowl(
    clock=InternalClock(tempo=config.bpm, bpb=config.beats),
)

# Starting the clock
bowl.start()

sleep = bowl.sleep

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
again = bowl.scheduler.schedule_func

# Adding a parser
# bowl.swap_parser(ListParser)

# Adding Senders
bowl.add_handler(MidiHandler())
dirt = SuperDirtHandler()
bowl.add_handler(dirt)
# bowl.add_handler(SuperColliderHandler(name="Custom SuperCollider Connexion"))
# bowl.add_handler(OSCHandler())

if CRASH_TEST:
    @swim
    def dummy_swimming_function():
        print('Hello there, I am swimming again!')
        M('60').out()
        S('bd').out()
        O('/hello/', value=1, other=2, otherother=3).out()

    Pa >> play('bd')
    Pb >> play_midi('60,67')
    Pc >> play_osc('/hello/surf/', value=1, other=2, otherother=3)
