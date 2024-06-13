from ..io.UserConfig import create_template_configuration_file
from InquirerPy.validator import EmptyInputValidator
from InquirerPy.base.control import Choice
from InquirerPy import inquirer
from rich.panel import Panel
from rich.table import Table
from pathlib import Path
from ..logger import print
from appdirs import *  # Wildcard used in docs
import click
import json
import mido
import os

FUNNY_TEXT = """
░█████╗░░█████╗░███╗░░██╗███████╗██╗░██████╗░
██╔══██╗██╔══██╗████╗░██║██╔════╝██║██╔════╝░
██║░░╚═╝██║░░██║██╔██╗██║█████╗░░██║██║░░██╗░
██║░░██╗██║░░██║██║╚████║██╔══╝░░██║██║░░╚██╗
╚█████╔╝╚█████╔╝██║░╚███║██║░░░░░██║╚██████╔╝
░╚════╝░░╚════╝░╚═╝░░╚══╝╚═╝░░░░░╚═╝░╚═════╝░

 This is the configuration tool for Sardine.
 This tool can configure the default session.
 Use it wisely, discover all the options!
"""

# Appdirs boilerplate code
APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
CONFIG_JSON = USER_DIR / "config.json"


def read_json_file():
    """Read JSON File (configuration file)"""
    with open(str(CONFIG_JSON), "r") as jsonFile:
        return json.load(jsonFile)


def write_json_file(data: dict):
    """Write to JSON File (configuration file)"""
    with open(str(CONFIG_JSON), "w") as jsonFile:
        json.dump(data, jsonFile, indent=4, sort_keys=True)


def _edit_configuration(file_name: str):
    configuration_file = USER_DIR / file_name
    # If the file already exists, we will read it first before opening editor
    if configuration_file.is_file():
        with open(configuration_file, "r") as config:
            file_content = config.read()
        edited = click.edit(file_content)
        if edited is not None:
            with open(configuration_file, "w+") as config:
                config.write(edited)
    else:
        try:
            open(configuration_file, "x")
        except FileExistsError:
            pass
        # recurse to write in the file
        _edit_configuration(file_name)


def edit_python_configuration():
    """Call $EDITOR to edit Python based user configuration"""
    _edit_configuration("user_configuration.py")


def edit_superdirt_configuration():
    """Call $EDITOR to edit Python based user configuration"""
    _edit_configuration("default_superdirt.scd")


def _select_midi_output(config_file: dict) -> dict:
    """
    Select a MIDI port. Provide custom options:
    - Manual selection (using mido for autocompletion)
    - Automatic selection (select Sardine port)
    - Custom port (write it at the command line)
    """

    choices = ["Automatic", "Manual", "Custom (advanced)"]
    midi_ports = mido.get_output_names()
    if sys.platform == "win32":
        for i, port in enumerate(midi_ports):
            midi_ports[i] = " ".join(port.split(" ")[:-1])
    print(
        Panel.fit(
            f"[red]Current MIDI Output: [green]{config_file['midi']}[/green][/red]"
        )
    )
    menu_select = inquirer.select(
        message="Select a method for choosing output port:", choices=choices
    ).execute()
    if menu_select == choices[1]:  # Manual selection
        midi_port_selection = inquirer.select(
            "Select a MIDI port in the following list:", choices=midi_ports
        ).execute()
    elif menu_select == choices[0]:  # Automatic selection
        midi_port_selection = "Sardine"
    elif menu_select == choices[2]:  # Custom selection
        midi_port_selection = inquirer.text(
            message="Enter your desired MIDI Port",
            completer={k: None for k in midi_ports},
            multicolumn_complete=True,
        ).execute()
    else:
        midi_port_selection = inquirer.text(
            message="Enter your desired MIDI Port",
            completer={k: None for k in midi_ports},
            multicolumn_complete=True,
        ).execute()
    config_file["midi"] = midi_port_selection
    print(
        Panel.fit(
            f"[red]Current MIDI Output: [green]{config_file['midi']}[/green][/red]"
        )
    )
    os.system("cls" if os.name == "nt" else "clear")
    return config_file


def _select_bpm_and_timing(config_file: dict) -> dict:
    """
    Selection of BPM and various Timing related information
    """
    print(
        Panel.fit(
            (
                f"[red]Tempo: [green]{config_file['bpm']}[/green][/red] | "
                + f"[red]Beats: [green]{config_file['beats']}[/green][/red] | "
                + f"[red]Link: [green]{config_file['link_clock']}[/green][/red]"
            )
        )
    )
    link_clock = inquirer.select(
        message="Should Sardine default to the LinkClock?",
        choices=[
            Choice(value=False, enabled=True, name="No (internal clock)"),
            Choice(value=True, name="Yes (external clock)"),
        ],
        default=None,
    ).execute()
    config_file["link_clock"] = link_clock
    tempo = inquirer.number(
        message="Input a new default tempo (BPM):",
        min_allowed=20.0,
        default=120.0,
        max_allowed=800,
        float_allowed=True,
        validate=EmptyInputValidator(),
    ).execute()
    config_file["bpm"] = float(tempo)
    beats = inquirer.number(
        message="Select a new number of beats per measure:",
        default=4,
        min_allowed=1,
        max_allowed=999,
    ).execute()
    config_file["beats"] = int(beats)
    print(
        Panel.fit(
            (
                f"[red]Tempo: [green]{config_file['bpm']}[/green][/red] | "
                + f"[red]Beats: [green]{config_file['beats']}[/green][/red] | "
                + f"[red]Link: [green]{config_file['link_clock']}[/green][/red]"
            )
        )
    )
    os.system("cls" if os.name == "nt" else "clear")
    return config_file


def _select_supercollider_settings(config_file: dict) -> dict:
    """Configuration for the SuperCollider subprocess"""
    print(
        Panel.fit(
            (
                f"[red]SuperDirt Handler: [green]{config_file['superdirt_handler']}[/red][/green] | "
                + f"[red]Boot SuperCollider: [green]{config_file['boot_supercollider']}[/red][/green] | "
                + f"[red]Sardine boot file: [green]{config_file['sardine_boot_file']}[/red][/green] | "
                + f"[red]SuperCollider boot Path: [green]{config_file['superdirt_config_path']}[/red][/green]"
            )
        )
    )
    boot = inquirer.select(
        message="Add SuperDirt handler to Sardine?",
        choices=[
            Choice(value=True, enabled=True, name="Yes"),
            Choice(value=False, name="No"),
        ],
        default=None,
    ).execute()
    config_file["superdirt_handler"] = boot

    boot_supercollider = inquirer.select(
        message="Boot a SuperCollider instance?",
        choices=[
            Choice(value=True, enabled=True, name="Yes"),
            Choice(value=False, name="No"),
        ],
        default=None,
    ).execute()
    config_file["boot_supercollider"] = boot_supercollider

    sardine_boot_file = inquirer.select(
        message="Use Sardine boot file (in config folder)?",
        choices=[
            Choice(value=True, enabled=True, name="Yes"),
            Choice(value=False, name="No"),
        ],
        default=None,
    ).execute()
    config_file["sardine_boot_file"] = sardine_boot_file

    verbose_superdirt = inquirer.select(
        message="Turn on verbose output for SuperCollider?",
        choices=[
            Choice(value=True, enabled=True, name="Yes"),
            Choice(value=False, name="No"),
        ],
        default=None,
    ).execute()
    config_file["verbose_superdirt"] = verbose_superdirt

    boot_path = inquirer.text(
        message="Enter your SuperDirt boot path\n\
(leave blank for default):"
    ).execute()
    if boot_path != "":
        config_file["superdirt_config_path"] = boot_path
    print(
        Panel.fit(
            (
                f"[red]SuperDirt Handler: [green]{config_file['superdirt_handler']}[/red][/green] | "
                + f"[red]Boot SuperCollider: [green]{config_file['boot_supercollider']}[/red][/green] | "
                + f"[red]Sardine boot file: [green]{config_file['sardine_boot_file']}[/red][/green] | "
                + f"[red]SuperCollider boot Path: [green]{config_file['superdirt_config_path']}[/red][/green]"
            )
        )
    )
    os.system("cls" if os.name == "nt" else "clear")
    return config_file


def _select_additional_options(config_file: dict) -> dict:
    """Select additionals options used by Sardine"""
    print(
        Panel.fit(
            (
                f"[red]Debug mode: [green]{config_file['debug']}[/green][/red] | "
                + f"[red]User config path: [green]{config_file['user_config_path']}[/green][/red]"
            )
        )
    )
    debug = inquirer.select(
        message="Turn on parser debug mode?",
        choices=[
            Choice(value=True, enabled=True, name="Yes"),
            Choice(value=False, name="No"),
        ],
        default=None,
    ).execute()
    config_file["debug"] = debug
    user_config_path = inquirer.text(
        message="Enter your user Python config file path\n\
(leave blank for default):"
    ).execute()
    if user_config_path != "":
        config_file["user_config_path"] = user_config_path
    print(
        Panel.fit(
            (
                f"[red]Debug mode: [green]{config_file['debug']}[/green][/red] | "
                + f"[red]User config path: [green]{config_file['user_config_path']}[/green][/red]"
            )
        )
    )
    os.system("cls" if os.name == "nt" else "clear")
    return config_file


def print_config(user_configuration: dict) -> None:
    """
    Configuration table format pretty printer
    """
    explanations = {
        "beats": "Number of beats per measure",
        "boot_supercollider": "Should Sardine boot SuperCollider?",
        "bpm": "Tempo in BPM",
        "debug": "Turn on parser debug mode (devs only)",
        "deferred_scheduling": "Use deferred scheduling (devs only)",
        "editor": "Should Sardine use its own editor?",
        "link_clock": "Should Sardine use Ableton Link Clock?",
        "midi": "Currently selected MIDI output",
        "parser": "Unused",
        "sardine_boot_file": "Should Sardine use its own boot file?",
        "superdirt_config_path": "Path to SuperDirt configuration file",
        "superdirt_handler": "Should Sardine use SuperDirt?",
        "user_config_path": "Path to user Python configuration file",
        "verbose_superdirt": "Turn on verbose output (console) for SuperCollider?",
    }
    table = Table(title="Current Sardine Configuration")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    table.add_column("?", style="yellow")
    for (key, value) in user_configuration.items():
        table.add_row(
            key, str(value), explanations[key] if key in explanations else "?"
        )
    print(table)


def main():
    """
    New point of entry for the configuration tool. It is now an hybrid between a
    TUI and CLI. Simple contextual menu that allows the user to change values in
    the JSON file without the need of writing too much. It is based on a very
    primitive while loop that ends when the user is done editing to its liking.

    Just like before, we are building a monolothic configuration dict that we
    inject into the current config.json file. Not fancy but cool nonetheless!
    """

    MENU_CHOICES = [
        "Show current configuration",
        "Select MIDI Output",
        "Select Musical Clock",
        "SuperCollider Options",
        "More options (devs)",
        "Reset configuration",
        "Exit",
    ]

    try:
        USER_CONFIG = read_json_file()["config"]
    except FileNotFoundError as e:
        print(
            "[bold red]No Sardine Configuration found. Please boot Sardine first![/bold red]"
        )
        exit()

    # This panel can stay because it is a splashscreen
    print(Panel.fit("[red]" + FUNNY_TEXT + "[/red]"))
    os.system("cls" if os.name == "nt" else "clear")

    while True:

        menu_select = inquirer.select(
            message="Select an option", choices=MENU_CHOICES
        ).execute()

        if menu_select == MENU_CHOICES[6]:
            os.system("cls" if os.name == "nt" else "clear")
            write_to_file = inquirer.confirm(
                message="Do you wish to save and exit?"
            ).execute()
            if write_to_file:
                try:
                    write_json_file({"config": USER_CONFIG})
                    exit()
                except Exception:
                    raise SystemError("Couldn't write config file!")
            os.system("cls" if os.name == "nt" else "clear")
        elif menu_select == MENU_CHOICES[5]:
            os.system("cls" if os.name == "nt" else "clear")
            create_template_configuration_file(CONFIG_JSON)
            USER_CONFIG = read_json_file()["config"]
        elif menu_select == MENU_CHOICES[0]:
            os.system("cls" if os.name == "nt" else "clear")
            print_config(USER_CONFIG)
        elif menu_select == MENU_CHOICES[1]:
            os.system("cls" if os.name == "nt" else "clear")
            USER_CONFIG = _select_midi_output(config_file=USER_CONFIG)
        elif menu_select == MENU_CHOICES[2]:
            os.system("cls" if os.name == "nt" else "clear")
            USER_CONFIG = _select_bpm_and_timing(config_file=USER_CONFIG)
        elif menu_select == MENU_CHOICES[3]:
            os.system("cls" if os.name == "nt" else "clear")
            USER_CONFIG = _select_supercollider_settings(config_file=USER_CONFIG)
        elif menu_select == MENU_CHOICES[4]:
            os.system("cls" if os.name == "nt" else "clear")
            USER_CONFIG = _select_additional_options(config_file=USER_CONFIG)
