from typing import TYPE_CHECKING
from ..base.handler import BaseHandler

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

class SleepHandler(BaseHandler):
    def __repr__(self) -> str:
        return f"SleepHandler"

    def setup(self):
        for event in ():  # TODO specify sleephandler events
            self.register(event)

    def hook(self, event: str, *args):
        ...  # TODO sleephandler hook()
