from typing import TYPE_CHECKING
from ..base.handler import BaseHandler
from ..io.MidiIo import MIDIIo

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

class MidiHandler(BaseHandler):
    def __init__(self):
        self.env = None

    def setup(self, env: 'FishBowl'):
        pass

    def hook(self, event: str, *args, **kwargs):
        pass