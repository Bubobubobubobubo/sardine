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
        # Not exactly a pleasing solution for multiple inheritance
        threading.Thread.__init__(self)
        BaseHandler.__init__(self)

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
            self.register(event)

    def hook(self, event: str, *args):
        func = self._events[event]
        func(*args)

    def _start(self, *args) -> None:
        self._midi.send(mido.Message("start"))

    def _continue(self, *args) -> None:
        self._midi.send(mido.Message("continue"))

    def _stop(self, *args) -> None:
        self._midi.send(mido.Message("stop"))

    def _reset(self, *args) -> None:
        self._midi.send(mido.Message("reset"))

    def _clock(self, *args) -> None:
        self._midi.send(mido.Message("clock"))

    def _note_on(self, channel: int, note: int, velocity: int) -> None:
        self._midi.send(mido.Message(
            'note_on', channel=channel, note=note, velocity=velocity))

    def _note_off(self, channel: int, note: int, velocity: int) -> None:
        self._midi.send(mido.Message(
            'note_off', channel=channel, note=note, velocity=velocity))

    def _polytouch(self, channel: int, note: int, value: int) -> None:
        self._midi.send(mido.Message(
            'polytouch', channel=channel, note=note, value=value))

    def _aftertouch(self, channel: int, value: int) -> None:
        self._midi.send(mido.Message(
            'aftertouch', channel=channel, value=value))

    def _control_change(self, channel: int, control: int, value: int) -> None:
        self._midi.send(mido.Message(
            'control_change', channel=channel, control=control, value=value))

    def _program_change(self, program: int, channel: int) -> None:
        self._midi.send(mido.Message(
            'program_change', program=program, channel=channel))

    def _sysex(self, data: bytearray, time: int = 0) -> None:
        self._midi.send(mido.Message("sysex", data=data, time=time))

    def _pitch_wheel(self, pitch: int, channel: int) -> None:
        self._midi.send(mido.Message( "pitchweel", pitch=pitch, channel=channel))