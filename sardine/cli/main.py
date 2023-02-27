from ..io.UserConfig import create_template_configuration_file
from InquirerPy.validator import EmptyInputValidator
from InquirerPy.base.control import Choice
from InquirerPy import inquirer
from rich.panel import Panel
from pathlib import Path
from ..logger import print
from appdirs import *  # Wildcard used in docs
import click
import json
import mido


FUNNY_TEXT = """
░█████╗░░█████╗░███╗░░██╗███████╗██╗░██████╗░
██╔══██╗██╔══██╗████╗░██║██╔════╝██║██╔════╝░
██║░░╚═╝██║░░██║██╔██╗██║█████╗░░██║██║░░██╗░
██║░░██╗██║░░██║██║╚████║██╔══╝░░██║██║░░╚██╗
╚█████╔╝╚█████╔╝██║░╚███║██║░░░░░██║╚██████╔╝
░╚════╝░░╚════╝░╚═╝░░╚══╝╚═╝░░░░░╚═╝░╚═════╝░

 This is the configuration tool for Sardine
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
    print(
        Panel.fit(
            (
                f"[red]Tempo: [green]{config_file['bpm']}[/green][/red] | "
                + f"[red]Beats: [green]{config_file['beats']}[/green][/red] | "
                + f"[red]Link: [green]{config_file['link_clock']}[/green][/red]"
            )
        )
    )
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
    return config_file


def _select_editor(config_file: dict) -> dict:
    """Select to spawn or not the embedded text editor"""
    editor = inquirer.select(
        message="Would you like to open up the embedded code editor?",
        choices=[
            Choice(value=True, enabled=True, name="Yes"),
            Choice(value=False, name="No"),
        ],
        default=None,
    ).execute()
    config_file["editor"] = editor
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

    MENU_CHOICES = [
        "Show Config",
        "Reset",
        "MIDI",
        "Clock",
        "SuperCollider",
        "Editor",
        "More",
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

    while True:

        menu_select = inquirer.select(
            message="Select an option",
            choices=MENU_CHOICES
        ).execute()

        if menu_select == "Exit":

            write_to_file = inquirer.confirm(
                message="Do you wish to save and exit?"
            ).execute()
            if write_to_file:
                try:
                    write_json_file({"config": USER_CONFIG})
                    exit()
                except Exception:
                    raise SystemError("Couldn't write config file!")
        elif menu_select == "Reset":
            create_template_configuration_file(CONFIG_JSON)
            USER_CONFIG = read_json_file()["config"]
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
        elif menu_select == "Editor":
            USER_CONFIG = _select_editor(config_file=USER_CONFIG)



if __name__ == "__main__":
    main()
