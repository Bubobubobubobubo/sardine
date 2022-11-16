from typing import TYPE_CHECKING
from ..base.handler import BaseHandler
from ..io.MidiIo import MIDIIo
import threading
import mido
import sys

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

class MidiHandler(BaseHandler, threading.Thread):

    """
    MidiHandler: a class capable of reacting to most MIDI Messages.
    """

    def __init__(self, port_name: str = "Sardine"):
        threading.Thread.__init__(self)

        # Setting up the MIDI Connexion
        self._available_ports = mido.get_output_names()
        self._port_name = port_name
        self._midi = None
        # For MacOS/Linux
        if sys.platform not in "win32":
            if self._port_name in ["Sardine", "internal"]:
                self._midi = mido.open_output("Sardine", virtual=True)
            else:
                self._midi = mido.open_output(self._available_ports[0], virtual=True)
                self._port_name = str(self._available_ports[0])
        # For W10/W11
        else:
            try:
                self._midi = mido.open_output(self._available_ports[0])
                self._port_name = str(self._available_ports[0])
            except Exception as err:
                print(f"[red]Failed to open a MIDI Connexion: {err}")

        # Setting up the handler
        self.env = None
        self.events = {
            'start': lambda: mido.Message('start'),
            'continue': lambda: mido.Message('continue'),
            'stop': lambda: mido.Message('stop'),
            'reset': lambda: mido.Message('reset'),
            'clock': lambda: mido.Message('clock'),
            'note_on': lambda args: mido.Message('note_on', *args),
            'note_off': lambda args: mido.Message('note_off', *args),
            'aftertouch': lambda args: mido.Message('aftertouch', *args),
            'control_change': lambda args: mido.Message('control_change', *args),
            'program_change': lambda args: mido.Message('program_change', *args),
            'sysex': lambda args: mido.Message('sysex', *args),
            'pitch_wheel': lambda args: mido.Message('pitchwheel', *args),
        }

    def __repr__(self) -> str:
        return f"{self._port_name}: MIDI Handler"


    def setup(self, env: 'FishBowl'):
        self.env = env

    def hook(self, event: str, *args, **kwargs):
        pass