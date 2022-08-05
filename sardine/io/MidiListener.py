import mido
from mido import (
        Message,
        open_input,
        get_input_names)
from rich import print
from typing import Optional
from time import sleep
from collections import deque


__all__ = ('MidiListener',)


class MidiListener():
    """MIDI-In Listener"""


    def __init__(self,
            port_name: Optional[str] = None):

        self.queue = deque(maxlen=20)
        self._last_item: Optional[Message] = None

        if port_name:
            try:
                self._input = open_input(port_name)
                self._input.callback = self._callback
                print(f"MidiListener: listening on port {port_name}")
            except Exception as e:
                print(f"{e}")
        else:
            try:
                self._input = open_input()
                self._input.callback = self._callback
                listened_port = mido.get_input_names()[0]
                print(f"MidiListener: listening on port {listened_port}")
            except Exception as e:
                pass


    def __str__(self):
        return f"<MidiListener: {self._input}>"


    def _callback(self, message):
        """Callback for MidiListener Port"""
        if message.is_cc():
            self.queue.append(message)


    def get(self):
        """Get an item from the MidiListener"""
        if self.queue:
            self._last_item = self.queue.pop()
        else:
            self._last_item = self._last_item

        return self._last_item


    def kill(self):
        """Close the MIDIListener"""
        self._input.close()
