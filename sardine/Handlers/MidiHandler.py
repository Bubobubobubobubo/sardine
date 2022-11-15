from typing import TYPE_CHECKING
from ..base.BaseHandler import BaseHandler
from ..io.MidiIo import MIDIIo

if TYPE_CHECKING:
    from ..FishBowl import FishBowl

class MidiHandler(BaseHandler):
    def __init__(self):
        pass

    def setup(self, env: 'FishBowl'):
        pass

    def hook(self, event: str, *args, **kwargs):
        pass