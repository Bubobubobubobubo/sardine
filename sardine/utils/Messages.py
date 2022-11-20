from rich.panel import Panel

sardine_intro = Panel.fit("""[red]
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
[/red]""")

def _ticked(condition: bool):
    """Print an ASCII Art [X] if True or [ ] if false"""
    return "[X]" if condition else "[ ]"

def config_line_printer(config: dict):
    return  (f"[yellow]BPM: [red]{config.bpm}[/red]," +
            f"[yellow]BEATS: [red]{config.beats}[/red] " +
            f"[yellow]SC: [red]{_ticked(config.superdirt_handler)}[/red], " +
            f"[yellow]DEFER: [red]{_ticked(config.deferred_scheduling)}[/red] " +
            f"[yellow]MIDI: [red]{config.midi}[/red]")