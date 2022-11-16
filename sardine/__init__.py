from rich import print
from rich.panel import Panel


import asyncio
import sys
import importlib
from pathlib import Path
import os
try:
    import uvloop
except ImportError:
    print("[yellow]UVLoop is not installed. Not supported on Windows![/yellow]")
    print("[yellow]Rhythm accuracy may be impacted[/yellow]")
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvloop.install()

from .FishBowl import FishBowl
from .clock.Time import Time
from .clock.InternalClock import Clock
from .clock.LinkClock import LinkClock
from .sequences.LexerParser.ListParser import ListParser
from .Handlers import (
    SuperColliderHandler,
    MidiHandler, OSCHandler)
from .sequences.Iterators import Iterator
from .sequences.Variables import Variables
from .superdirt.AutoBoot import SuperColliderProcess

from .io.UserConfig import (
    read_user_configuration,
    pretty_print_configuration_file)
config = read_user_configuration()

#| INITIALISATION |#

# Reading user configuration
config = read_user_configuration()
print_config = pretty_print_configuration_file
sardine_intro = """
░██████╗░█████╗░██████╗░██████╗░██╗███╗░░██╗███████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║████╗░██║██╔════╝
╚█████╗░███████║██████╔╝██║░░██║██║██╔██╗██║█████╗░░
░╚═══██╗██╔══██║██╔══██╗██║░░██║██║██║╚████║██╔══╝░░
██████╔╝██║░░██║██║░░██║██████╔╝██║██║░╚███║███████╗
╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝╚══════╝

Sardine is a MIDI/OSC sequencer made for live-coding
Play music, read the docs, contribute, and have fun!
WEBSITE: [yellow]https://sardine.raphaelforment.fr[/yellow]
GITHUB: [yellow]https://github.com/Bubobubobubobubo/sardine[/yellow]
"""

from sys import argv
hook_path = argv[0]
if "__main__.py" in hook_path:
    os.environ["SARDINE_INIT_SESSION"] = "YES"

if (
    os.getenv("SARDINE_INIT_SESSION") is not None
    and os.getenv("SARDINE_INIT_SESSION") == "YES"
):
    def _ticked(condition: bool):
        """Print an ASCII Art [X] if True or [ ] if false"""
        return "[X]" if condition else "[ ]"
    print(Panel.fit(f"[red]{sardine_intro}[/red]"))
    print(
        f" [yellow]BPM: [red]{config.bpm}[/red],",
        f"[yellow]BEATS: [red]{config.beats}[/red]",
        f"[yellow]SC: [red]{_ticked(config.boot_superdirt)}[/red],",
        f"[yellow]DEFER: [red]{_ticked(config.deferred_scheduling)}[/red]",
        f"[yellow]MIDI: [red]{config.midi}[/red]",
    )

    # Boot SuperCollider
    if config.boot_superdirt is True:
        try:
            SC = SuperColliderProcess(
                startup_file=config.superdirt_config_path,  # config file
                verbose=config.verbose_superdirt,  # verbosity for SC output
            )
        except OSError as error:
            print("[red]SuperCollider could not be found![/red]")
    else:
        print("[green]Booting without SuperCollider![/green]")

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


    bowl = FishBowl(time=Time())
    time = bowl.time # passage of time
    bowl.clock.tempo, bowl.clock._beats_per_bar = config.bpm, config.beats

    # Adding a parser
    bowl.swap_parser(ListParser)

    # Adding Senders
    bowl.add_handler(MidiHandler())
    bowl.add_handler(OSCHandler())
    bowl.add_handler(SuperColliderHandler())

    # Start clock
    bowl.clock.start()