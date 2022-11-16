from typing import TYPE_CHECKING
from ..base.handler import BaseHandler

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

class DummyHandler(BaseHandler):
    def __init__(self, ip: str = "127.0.0.1", port: int = 23456):
        self._ip, self._port = (ip, port)
        self.env = None
        self._events = {
            'bleep': self._bleep,
            'bloop': self._bloop,
        }

    def __repr__(self) -> str:
        return f"OSCHandler: {self._ip}:{self._port}"

    def setup(self):
        for event in self._events:
            self.env.register_hook(event, self)

    def hook(self, event: str, *args, **kwargs):
        func = self.events[event]
        func(*args, **kwargs)

    def _bleep(self, *args, **kwargs):
        print(f'bleep: {args}, {kwargs}')

    def _bloop(self, *args, **kwargs):
        print(f'bloop: {args}, {kwargs}')