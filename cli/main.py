import argparse
import click
import mido
import json
import sys

# Wildcard used in docs..
from appdirs import *
from pathlib import Path
from rich import print
from rich.panel import Panel
from itertools import chain
from InquirerPy import inquirer, prompt
from InquirerPy.validator import EmptyInputValidator
from InquirerPy.base.control import Choice

FUNNY_TEXT = """
░█████╗░░█████╗░███╗░░██╗███████╗██╗░██████╗░
██╔══██╗██╔══██╗████╗░██║██╔════╝██║██╔════╝░
██║░░╚═╝██║░░██║██╔██╗██║█████╗░░██║██║░░██╗░
██║░░██╗██║░░██║██║╚████║██╔══╝░░██║██║░░╚██╗
╚█████╔╝╚█████╔╝██║░╚███║██║░░░░░██║╚██████╔╝
░╚════╝░░╚════╝░╚═╝░░╚══╝╚═╝░░░░░╚═╝░╚═════╝░

 This is the configuration tool for Sardine
"""


# def str2bool(v):
#     """Boolean validation method for argparse type checking"""
#     if v.lower() in ("yes", "true", "t", "y", "1"):
#         return True
#     elif v.lower() in ("no", "false", "f", "n", "0"):
#         return False
#     else:
#         raise argparse.ArgumentTypeError("Boolean value expected.")
#
#
# def pairwise(iterable):
#     """s -> (s0, s1), (s2, s3), (s4, s5), ..."""
#     a = iter(iterable)
#     return zip(a, a)


# ============================================================================ #
# A dead simple argparse configuration tool to edit values stored in config.json
# Automatic type-checking / error raising for each value.
# ============================================================================ #

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


# def old_main():
#     """Entry method for the argparse parser"""
#
#     # Check if the configuration file exists, otherwise, warn user
#     if not CONFIG_JSON.is_file():
#         print(
#             f"[red]The configuration file is missing.\
#  Please boot Sardine first."
#         )
#         exit()
#     data = read_json_file()
#
#     parser = argparse.ArgumentParser(description="Sardine configuration CLI")
#     parser.add_argument("--midi", type=str, help="Default MIDI port")
#     parser.add_argument("--bpm", type=float, help="Beats per minute")
#     parser.add_argument("--beats", type=int, help="Beats per bar")
#     parser.add_argument("--ppqn", type=float, help="ppqn")
#     parser.add_argument("--boot_superdirt", type=str2bool, help="Boot SC && SuperDirt")
#     parser.add_argument("--debug", type=str2bool, help="Parser debugging mode")
#     parser.add_argument(
#         "--verbose_superdirt", type=str2bool, help="Toggle SuperDirt textual output"
#     )
#     parser.add_argument(
#         "--deferred_scheduling", type=str2bool, help="Turn on/off deferred scheduling"
#     )
#     parser.add_argument("--active_clock", type=str2bool, help="Active or passive Clock")
#     parser.add_argument(
#         "--SCconfig", type=str2bool, help="SuperDirt Configuration Path"
#     )
#     parser.add_argument(
#         "--User Config Path", type=bool, help="Python User Configuration file"
#     )
#
#     if len(sys.argv) < 2:
#         print(f"[red]{FUNNY_TEXT}")
#         print(f"Your configuration file is located at: {USER_DIR}")
#         parser.print_help()
#         exit()
#
#     # Grabing arguments from parser.parse_args()
#     args = parser.parse_args()
#     to_update = list(chain.from_iterable([x for x in args._get_kwargs()]))
#
#     # Iterating over the collected kwargs and write to file if needed
#     for name, value in pairwise(to_update):
#         if value is not None:
#             data["config"][name] = value
#     write_json_file(data)
#
#
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
                + f"[red]PPQN: [green]{config_file['ppqn']}[/green][/red]"
            )
        )
    )
    active_clock = inquirer.select(
        message="Should the Clock be active or passive?",
        choices=[
            Choice(value=True, enabled=True, name="Active (default)"),
            Choice(value=False, name="Passive (for MIDI In)"),
        ],
        default=None,
    ).execute()
    config_file["active_clock"] = active_clock
    tempo = inquirer.number(
        message="Input a new default tempo (BPM):",
        min_allowed=20,
        max_allowed=800,
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
    ppqn = inquirer.number(
        message="Select a new number of ppqn (Pulses per Quarter Note):",
        min_allowed=1,
        max_allowed=999,
        default=48,
        float_allowed=False,
    ).execute()
    config_file["ppqn"] = int(ppqn)
    print(
        Panel.fit(
            (
                f"[red]Tempo: [green]{config_file['bpm']}[/green][/red] | "
                + f"[red]Beats: [green]{config_file['beats']}[/green][/red] | "
                + f"[red]PPQN: [green]{config_file['ppqn']}[/green][/red]"
            )
        )
    )
    return config_file


def _select_supercollider_settings(config_file: dict) -> dict:
    """Configuration for the SuperCollider subprocess"""
    print(
        Panel.fit(
            (
                f"[red]Boot SuperCollider: [green]{config_file['boot_superdirt']}[/red][/green] | "
                + f"[red]SuperCollider boot Path: [green]{config_file['superdirt_config_path']}[/red][/green]"
            )
        )
    )
    boot = inquirer.select(
        message="Boot SuperCollider along with Sardine?",
        choices=[
            Choice(value=True, enabled=True, name="Yes"),
            Choice(value=False, name="No"),
        ],
        default=None,
    ).execute()
    config_file["boot_superdirt"] = boot
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
                f"[red]Boot SuperCollider: [green]{config_file['boot_superdirt']}[/red][/green] | "
                + f"[red]SuperCollider boot Path: [green]{config_file['superdirt_config_path']}[/red][/green]"
            )
        )
    )
    return config_file


def _select_additional_options(config_file: dict) -> dict:
    """Select additionals options used by Sardine"""
    print(
        Panel.fit(
            (
                f"[red]Debug mode: [green]{config_file['boot_superdirt']}[/green][/red] | "
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
                f"[red]Debug mode: [green]{config_file['boot_superdirt']}[/green][/red] | "
                + f"[red]User config path: [green]{config_file['user_config_path']}[/green][/red]"
            )
        )
    )
    return config_file


def main():
    """
    New point of entry for the configuration tool. It is now an hybrid between a
    TUI and CLI. Simple contextual menu that allows the user to change values in
    the JSON file without the need of writing too much. It is based on a very
    primitive while loop that ends when the user is done editing to its liking.

    Just like before, we are building a monolothic configuration dict that we
    inject into the current config.json file. Not fancy but cool nonetheless!
    """
    MENU_CHOICES = ["Show Config", "MIDI", "Clock", "SuperCollider", "More", "Exit"]
    try:
        USER_CONFIG = read_json_file()["config"]
    except FileNotFoundError as e:
        print(
            "[bold red]No Sardine Configuration found. Please boot Sardine first![/bold red]"
        )
        exit()
    print(Panel.fit("[red]" + FUNNY_TEXT + "[/red]"))
    while True:
        menu_select = inquirer.select(
            message="Select an option", choices=MENU_CHOICES
        ).execute()
        if menu_select == "Exit":
            write_to_file = inquirer.confirm(
                message="Do you wish to save the current config file?"
            ).execute()
            if write_to_file:
                try:
                    write_json_file({"config": USER_CONFIG})
                except Exception:
                    raise SystemError("Couldn't write config file!")
            exit_from_conf = inquirer.confirm(message="Do you wish to exit?").execute()
            if exit_from_conf:
                exit()
            else:
                continue
        elif menu_select == "Show Config":
            print(USER_CONFIG)
        elif menu_select == "MIDI":
            USER_CONFIG = _select_midi_output(config_file=USER_CONFIG)
        elif menu_select == "Clock":
            USER_CONFIG = _select_bpm_and_timing(config_file=USER_CONFIG)
        elif menu_select == "SuperCollider":
            USER_CONFIG = _select_supercollider_settings(config_file=USER_CONFIG)
        elif menu_select == "More":
            USER_CONFIG = _select_additional_options(config_file=USER_CONFIG)


if __name__ == "__main__":
    main()
