from appdirs import *
from pathlib import Path
from rich.console import Console

__all__ = ("print", )

APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
LOG_FILE = USER_DIR / "sardine.log"


report_file = open(LOG_FILE, "wt")
file_console = Console(file=report_file)

terminal_console = Console()

def print(*args, **kwargs):
    file_console.print(*args, **kwargs)
    terminal_console.print(*args, **kwargs)
