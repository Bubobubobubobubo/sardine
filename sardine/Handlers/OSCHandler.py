from typing import TYPE_CHECKING
from ..base.handler import BaseHandler

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl


class OSCHandler(BaseHandler):
    def __init__(self, ip: str = "127.0.0.1", port: int = 23456):
        self._ip, self._port = (ip, port)
        self.env = None

    def __repr__(self) -> str:
        return f"OSCHandler: {self._ip}:{self._port}"

    def setup(self, env: 'FishBowl'):
        self.env = env

    def hook(self, event: str, *args, **kwargs):
        pass