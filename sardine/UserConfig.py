import json
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from appdirs import *
from rich import print

__all__ = (
    "Config",
    "create_template_configuration_file",
    "read_configuration_file",
    "read_user_configuration",
    "pretty_print_configuration_file",
)

APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))

TEMPLATE_CONFIGURATION = {
    "config": {
        "midi": None,
        "bpm": 125,
        "beats": 4,
        "parameters": [],
        "parser": str,
        "superdirt_handler": True,
        "boot_supercollider": True,
        "sardine_boot_file": True,
        "verbose_superdirt": False,
        "link_clock": False,
        "superdirt_config_path": str(USER_DIR / "default_superdirt.scd"),
        "user_config_path": str(USER_DIR / "user_configuration.py"),
        "editor": False,
    }
}


def _recursive_update(dest: dict, src: dict):
    """Recursively updates the `dest` dictionary in-place using `src`."""
    for k, vsrc in src.items():
        vdest = dest.get(k)
        if isinstance(vdest, dict) and isinstance(vsrc, dict):
            _recursive_update(vdest, vsrc)
        else:
            dest[k] = vsrc


@dataclass
class Config:
    midi: Union[str, None]
    beats: int
    parameters: list
    bpm: int
    parser: str
    superdirt_config_path: str
    verbose_superdirt: bool
    user_config_path: str
    boot_supercollider: bool
    superdirt_handler: bool
    sardine_boot_file: bool
    link_clock: bool
    editor: bool

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        config = data["config"]
        return cls(
            midi=config["midi"],
            beats=config["beats"],
            parameters=config["parameters"],
            bpm=config["bpm"],
            parser=config["parser"],
            superdirt_handler=config["superdirt_handler"],
            boot_supercollider=config["boot_supercollider"],
            sardine_boot_file=config["sardine_boot_file"],
            verbose_superdirt=config["verbose_superdirt"],
            link_clock=config["link_clock"],
            superdirt_config_path=config["superdirt_config_path"],
            user_config_path=config["user_config_path"],
            editor=config["editor"],
        )

    def to_dict(self) -> dict:
        return {
            "config": {
                "midi": self.midi,
                "beats": self.beats,
                "parameters": self.parameters,
                "bpm": self.bpm,
                "parser": self.parser,
                "superdirt_handler": self.superdirt_handler,
                "boot_supercollider": self.boot_supercollider,
                "sardine_boot_file": self.sardine_boot_file,
                "verbose_superdirt": self.verbose_superdirt,
                "superdirt_config_path": self.superdirt_config_path,
                "link_clock": self.link_clock,
                "user_config_path": self.user_config_path,
                "editor": self.editor,
            }
        }


def write_configuration_file(config: Config, file_path: Path):
    """Write config JSON file"""
    with open(file_path, "w") as file:
        json.dump(config.to_dict(), file, indent=4, sort_keys=True)


def create_template_configuration_file(file_path: Path) -> Config:
    """If no configuration file is found, create a template"""
    config = Config.from_dict(TEMPLATE_CONFIGURATION)
    write_configuration_file(config, file_path)
    return config


def read_configuration_file(file_path: Path) -> Config:
    """Read config JSON File"""
    base = TEMPLATE_CONFIGURATION.copy()
    with open(file_path, "r") as f:
        user_data = json.load(f)
    _recursive_update(base, user_data)

    config = Config.from_dict(base)

    # Write any missing keys back to file
    write_configuration_file(config, file_path)

    return config


def pretty_print_configuration_file() -> None:
    file_path = USER_DIR / "config.json"
    file_string = read_configuration_file(file_path)
    print(file_string)


def read_user_configuration() -> Config:
    """Read or create user configuration file"""
    config_file = USER_DIR / "config.json"
    config = None

    # Check if the configuration folder exists
    if USER_DIR.is_dir():
        if config_file.exists():
            config = read_configuration_file(config_file)
        else:
            config = create_template_configuration_file(config_file)
    # If the configuration folder doesn't exist, create it and create config
    else:
        USER_DIR.mkdir(parents=True)
        config = create_template_configuration_file(config_file)
    return config


if __name__ == "__main__":
    config = read_user_configuration()
