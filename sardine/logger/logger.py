import logging
from appdirs import *
from pathlib import Path
import json
import logging.config
from rich.console import Console
from rich.logging import RichHandler
from logging.handlers import RotatingFileHandler

__all__ = ("print", "logging")

APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
LOG_FILE = USER_DIR / "sardine.log"

terminal_console = Console()

def print(*args, **kwargs):
    terminal_console.print(*args, **kwargs)

CONFIG = '''
{
   "version":1,
   "disable_existing_loggers":true,
   "formatters":{
      "rich_format":{
         "format":"%(message)s"
      },
      "file_format":{
         "format":"%(asctime)s | %(levelname)s | %(message)s",
         "datefmt":"%d/%m/%Y %H:%M:%S"
      }
   },
   "handlers":{
      "rich_handler":{
         "class":"rich.logging.RichHandler",
         "level":"WARNING",
         "formatter":"rich_format",
         "show_time": false,
         "show_path": false,
         "markup": true
      },
      "file_handler":{
         "class":"logging.handlers.RotatingFileHandler",
         "level":"NOTSET",
         "formatter":"file_format",
         "filename":"test_file",
         "maxBytes":50000,
         "backupCount":5,
         "encoding": "utf8"
      }
   },
   "loggers":{
        "":{
            "level": "DEBUG",
            "handlers":[
                "file_handler",
                "rich_handler"
            ],
            "propagate": true
        }
   }
}
'''

# load the JSON config and overwrite the filename variable to accept a variable path
config = json.loads(CONFIG)
config["handlers"]["file_handler"]["filename"] = LOG_FILE
logging.config.dictConfig(config)
