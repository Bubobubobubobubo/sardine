from typing import TYPE_CHECKING
from ..base.handler import BaseHandler

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

class SuperColliderHandler(BaseHandler):
    def __init__(self, ip: str = "127.0.0.1", port: int =  57120):
        self._ip, self._port = (ip, port)
        self.env = None
        self.events = {
            'play': lambda: print('Playing something')
        }

    def __repr__(self) -> str:
        return f"SCHandler: {self._ip}:{self._port}"

    def setup(self, env: 'FishBowl'):
        self.env = env

    def hook(self, event: str, *args, **kwargs):
        pass