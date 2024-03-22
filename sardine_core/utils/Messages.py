from rich.panel import Panel
import os

sardine_intro = """[red]
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
[/red]"""


def _ticked(condition: bool):
    """Print an ASCII Art [X] if True or [ ] if false"""
    return "[X]" if condition else "[ ]"


def greeter_printer(intro_logo: str, config: dict):
    os.system("cls" if os.name == "nt" else "clear")
    midi_port = "Automatic" if config.midi == "Sardine" else config.midi
    config_message = (
        f"[yellow]BPM: [red]{config.bpm}[/red] "
        + f"[yellow]BEATS: [red]{config.beats}[/red] "
        + f"[yellow]SC: [red]{_ticked(config.superdirt_handler)}[/red], "
        + f"[yellow]BOOT: [red]{_ticked(config.boot_supercollider)}[/red], "
        + f"[yellow]MIDI: [red]{config.midi}[/red]"
    )
    return Panel.fit(sardine_intro + "\n" + config_message)
