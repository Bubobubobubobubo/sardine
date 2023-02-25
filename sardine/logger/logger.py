import logging
from appdirs import *
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
from logging.handlers import RotatingFileHandler

__all__ = ("print", )

APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
LOG_FILE = USER_DIR / "sardine.log"

# Logging file for testing
TEST_FILE = USER_DIR / "test.log"

# The file needs to exist to actually log something
if not LOG_FILE.exists():
    LOG_FILE.touch()

# Actual logging logic
report_file = open(LOG_FILE, "wt", encoding="utf-8")
file_console = Console(file=report_file)

terminal_console = Console()

def print(*args, **kwargs):
    file_console.print(*args, **kwargs)
    terminal_console.print(*args, **kwargs)

# Implementation logging lib
console_fmt = "%(asctime)s | %(levelname)s | %(message)s"
datefmt = "%d/%m/%Y %H:%M:%S"

log = logging.getLogger('root')
log.setLevel(logging.DEBUG)

ch = RichHandler(level=logging.DEBUG, show_level=False, show_time=False, markup=True)
ch.setLevel(logging.DEBUG)
# this goes inside the rich format, I want it to define it entirely:
ch.setFormatter(logging.Formatter(console_fmt, datefmt))
log.addHandler(ch)

# just to show my existing default format as a 2nd line
ch = RotatingFileHandler(
    TEST_FILE,
    maxBytes=1000000, # set the maximum file size before creating a new one
    backupCount=5) # set the maximum number of log file before errasing the oldest
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter(console_fmt, datefmt))
log.addHandler(ch)

if __name__ == "__main__":
    log.info({"array": [1,2,3,4], "dict": {'one': 1, 'two': 2, 'three':3}, 'ok': True, 'notok': False})

