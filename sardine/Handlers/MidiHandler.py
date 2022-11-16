from typing import TYPE_CHECKING
from ..base.handler import BaseHandler
from ..io.MidiIo import MIDIIo
from mido import Message

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

class MidiHandler(BaseHandler):

    """
    MidiHandler: a class capable of reacting to most MIDI Messages.
    """
    def __init__(self):
        self.env = None
        self.events = {
            'start': lambda args: Message('start'),
            'continue': lambda args: Message('continue'),
            'stop': lambda args: Message('stop'),
            'reset': lambda args: Message('reset'),
            'clock': lambda args: Message('clock'),
            'note_on': lambda args: Message('note_on', *args),
            'note_off': lambda args: Message('note_off', *args),
            'aftertouch': lambda args: Message('aftertouch', *args),
            'control_change': lambda args: Message('control_change', *args),
            'program_change': lambda args: Message('program_change', *args),
            'sysex': lambda args: Message('sysex', *args),
            'pitch_wheel': lambda args: Message('pitchwheel', *args),
        }

    def setup(self, env: 'FishBowl'):
        self.env = env

    def hook(self, event: str, *args, **kwargs):
        pass