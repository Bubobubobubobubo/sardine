from typing import TYPE_CHECKING
from ..base.handler import BaseHandler

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl


class SuperColliderHandler(BaseHandler):
    def __init__(self, name: str, ip: str = "127.0.0.1", port: int = 23456):
        super().__init__()
        self._ip, self._port, self._name = (ip, port, name)
        # Open the client here

    def __repr__(self) -> str:
        return f"SCHandler: '{self._name}': [{self._ip}:{self._port}]"

    def hook(self, event: str, *args, **kwargs):
        pass