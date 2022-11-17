from typing import TYPE_CHECKING
from ..base.handler import BaseHandler

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

class SleepHandler(BaseHandler):
    def __init__(self, env: 'FishBowl'):
        self._env = env
        self._events = {
            '???': None
        }

    def __repr__(self) -> str:
        return f"SleepHandler"

    def setup(self):
        for event in self._events:
            self.register(event)

    def hook(self, event: str, *args):
        func = self._events[event]
        func(*args)