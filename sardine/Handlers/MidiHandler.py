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
            'start': self._start,
            'continue': self._continue,
            'stop': self._stop,
            'reset': self._reset,
            'clock': self._clock,
            'note_on': self._note_on,
            'note_off': self._note_off,
            'aftertouch': self._aftertouch,
            'polytouch': self._polytouch,
            'control_change': self._control_change,
            'program_change': self._program_change,
            'sysex': self._sysex,
            'pitch_wheel': self._pitchwheel,
        }

    def __repr__(self) -> str:
        return f"{self._port_name}: MIDI Handler"

    def setup(self):
        for event in self._events:
            self.env.register_hook(event, self)

    def hook(self, event: str, *args, **kwargs):
        func = self._events[event]
        func(*args, **kwargs)

    def _start(self, *args, **kwargs):
        self._midi.send(mido.Message("start"))

    def _continue(self, *args, **kwargs):
        self._midi.send(mido.Message("continue"))

    def _stop(self, *args, **kwargs):
        self._midi.send(mido.Message("stop"))

    def _reset(self, *args, **kwargs):
        self._midi.send(mido.Message("reset"))
    
    def _clock(self, *args, **kwargs):
        self._midi.send(mido.Message("clock"))

    def _note_on(self, *args, **kwargs):
        self._midi.send(mido.Message(
            'note_on',
            channel=int(kwargs['channel']),
            note=int(kwargs['note']),
            velocity=int(kwargs['velocity']),
        ))

    def _polytouch(self, *args, **kwargs):
        self._midi.send(mido.Message(
            'polytouch',
            channel=int(kwargs['channel']),
            note=int(kwargs['note']),
            value=int(kwargs['value']),
        ))

    def _note_off(self, *args, **kwargs):
        self._midi.send(mido.Message(
            'note_off',
            channel=int(kwargs['channel']),
            note=int(kwargs['note']),
            velocity=int(kwargs['velocity']),
        ))

    def _aftertouch(self, *args, **kwargs):
        self._midi.send(mido.Message(
            'aftertouch',
            channel=int(kwargs['channel']),
            value=int(kwargs['value']),
        ))

    def _control_change(self, *args, **kwargs) -> None:
        self._midi.send(mido.Message(
            'control_change',
            channel=int(kwargs['channel']),
            control=int(kwargs['control']),
            value=int(kwargs['value']),
        ))

    def _program_change(self, *args, **kwargs) -> None:
        self._midi.send(mido.Message(
            'program_change',
            program=int(kwargs['program']),
            channel=int(kwargs['channel']),
        ))

    def _sysex(self, *args, **kwargs) -> None:
        self._midi.send(mido.Message(
            "sysex", 
            data=bytearray(kwargs['data']), 
            time=int(0))
        )

    def _pitch_wheel(self, *args, **kwargs) -> None:
        self._midi.send(mido.Message(
            "pitchweel", 
            pitch=int(kwargs['pitch']), 
            channel=int(kwargs['channel'])
        )