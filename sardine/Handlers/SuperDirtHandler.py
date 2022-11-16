from typing import TYPE_CHECKING
from ..base.handler import BaseHandler
from ..superdirt.AutoBoot import SuperDirtProcess
from ..io import read_user_configuration

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

class SuperDirtHandler(BaseHandler):
    def __init__(self, ip: str = "127.0.0.1", port: int =  57120, name: str = 'SuperDirt'):
        super().__init__()
        self._ip, self._port, self._name = (ip, port, name)

        # Opening the OSC Client
        try:
            config = read_user_configuration()
            self._superdirt_process = SuperDirtProcess(
                startup_file=config.superdirt_config_path,
                verbose=config.verbose_superdirt
            )
        except OSError as Error:
            print(f"[red]SuperCollider could not be found: {Error}![/red]")

        # Setting up environment
        self.env = None
        self.events = {
            'play': lambda: print('Playing something'),
            'hush': lambda: print('Use the hush function'),
            'panic': lambda: print('Use the panic function')
        }

    def __repr__(self) -> str:
        return f"SuperDirt: {self._ip}:{self._port}"

    def hook(self, event: str, *args, **kwargs):
        pass
