import mido
from mido import open_output

class MidiListener():

    """
    MIDI-In Listener
    """

    def __init__(self, port_name: str):
        self._port_name = port_name
        try:
            self._midi = mido.open_output(port_name)
        except Exception as error:
            print(f"[red]Cannot listen to port {self._port_name}[/red]")