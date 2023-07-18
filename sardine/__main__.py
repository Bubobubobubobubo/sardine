from sardine.console import ConsoleManager
import click
import importlib.metadata
import os
import psutil
from typing import Tuple


def set_python_process_priority() -> Tuple[int, int, bool]:
    """
    Sets the priority of the current Python interpreter process
    to the highest possible level on Linux, macOS, and Windows.

    Returns:
        A tuple containing the original priority, new priority,
        and a boolean indicating whether the priority was
        successfully set.
    """
    pid = os.getpid()

    process = psutil.Process(pid)
    original_priority = process.nice()

    # Determine the new priority (lower values indicate higher priority)
    if os.name == "nt":
        new_priority = psutil.HIGH_PRIORITY_CLASS
    else:
        new_priority = -20

    try:
        process.nice(new_priority)
        success = True
    except (PermissionError, psutil.AccessDenied):
        success = False

    return original_priority, new_priority, success


_, _, successful_patch = set_python_process_priority()
# if successful_patch:
#     print(f"Patched process", end=" | ")
# else:
#     print("Unpatched process", end=" | ")

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}


@click.group(
    context_settings=CONTEXT_SETTINGS,
    help="Starts sardine in an asyncio REPL.",
    invoke_without_command=True,
)
@click.version_option(
    package_name="sardine",
    # prog_name=__package__,
    prog_name="sardine",
    message="%(prog)s for %(package)s v%(version)s",
)
@click.pass_context
def main(ctx: click.Context):
    if ctx.invoked_subcommand is None:
        console = ConsoleManager()
        console.start()


@main.command(
    short_help="Starts sardine configuration tool",
    help="This command starts Sardine configuration tool.",
)
def config():
    """Start sardine.cli:main from fishery"""
    from sardine_core.cli import main

    main()


@main.command(
    short_help="Open SuperDirt configuration file",
    help="This command opens the SuperDirt configuration file with your default editor.",
)
def config_superdirt():
    """Start sardine.cli:main from fishery"""
    from sardine_core.cli.main import edit_superdirt_configuration

    edit_superdirt_configuration()


@main.command(
    short_help="Open Python configuration file",
    help="This command opens the Python configuration file with your default editor.",
)
def config_python():
    """Start sardine.cli:main from fishery"""
    from sardine_core.cli.main import edit_python_configuration

    edit_python_configuration()


def run_pre_hooks() -> None:
    entry_points = importlib.metadata.entry_points(group="sardine.cli_main_hooks")
    for ep in entry_points:
        hook = ep.load()
        hook(main)


if __name__ == "__main__":
    main()
