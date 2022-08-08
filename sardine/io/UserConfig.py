from dataclasses import dataclass
import json
from pathlib import Path
from typing import Union

from appdirs import *
from rich import print

__all__ = (
    'Config', 'create_template_configuration_file',
    'read_configuration_file', 'read_user_configuration'
)

APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))

TEMPLATE_CONFIGURATION = {
    'config': {
        'midi': None,
        'bpm': 125,
        'beats': 4,
        'ppqn': 48,
        'parameters': [],
        'superdirt_config_path': str(USER_DIR / "default_superdirt.scd"),
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
    ppqn: int
    bpm: int
    superdirt_config_path: str

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        config = data['config']
        return cls(
            midi=config['midi'],
            beats=config['beats'],
            parameters=config['parameters'],
            ppqn=config['ppqn'],
            bpm=config['bpm'],
            superdirt_config_path=config['superdirt_config_path']
        )


def create_template_configuration_file(file_path: Path) -> Config:
    """ If no configuration file is found, create a template """
    with open(file_path, 'w') as file:
        json.dump(TEMPLATE_CONFIGURATION, file)
    return Config.from_dict(TEMPLATE_CONFIGURATION)


def read_configuration_file(file_path: Path) -> Config:
    """ Read config JSON File """
    base = TEMPLATE_CONFIGURATION.copy()
    with open(file_path, 'r') as f:
        user_data = json.load(f)
    _recursive_update(base, user_data)
    return Config.from_dict(base)


def read_user_configuration() -> Config:
    """ Read or create user configuration file """
    config_file = USER_DIR / "config.json"
    config = None

    # Check if the configuration folder exists
    if USER_DIR.is_dir():
        print(f"[green][1/3] Found configuration folder at {USER_DIR}[/green]")

        if config_file.exists():
            print(f"[green][2/3] Found configuration file[/green]")
            config = read_configuration_file(config_file)
        else:
            print(f"[green][2/3] Creating configuration file[/green]")
            config = create_template_configuration_file(config_file)

    # If the configuration folder doesn't exist, create it and create config
    else:
        print(f"[green][1/3] Creating configuration folder[/green]")
        USER_DIR.mkdir(parents=True)

        print(f"[green][2/3] Creating configuration file[/green]")
        config = create_template_configuration_file(config_file)

    print("[green][3/3] Returning configuration[/green]")
    return config

if __name__ == "__main__":
    config = read_user_configuration()
