import mido
from mido import (
        Message,
        open_input,
        get_input_names,
        parse_string_stream)
from rich import print
from typing import Optional, Union
from collections import deque
from dataclasses import dataclass


__all__ = (
        'MidiListener',
        'ClockListener',
        'ControlTarget',
        'NoteTarget')


@dataclass
class ControlTarget:
    control: int
    channel: int


@dataclass
class NoteTarget:
    channel: int


class MidiListener():
    """MIDI-In Listener"""


    def __init__(self,
            target: Union[ControlTarget, NoteTarget, None] = None,
            port: Optional[str] = None):

        self.target = target

        self.queue = deque(maxlen=20)
        self._last_item: Optional[Message] = None
        self._last_value= 0

        if port:
            try:
                self._input = open_input(port)
                self._input.callback = self._callback
                print(f"MidiListener: listening on port {port}")
            except Exception:
                raise OSError(f"Couldn't listen on port {port}")
        else:
            try:
                self._input = open_input()
                self._input.callback = self._callback
                listened_port = mido.get_input_names()[0]
                print(f"MidiListener: listening on port {listened_port}")
            except Exception:
                raise OSError(f"Couldn't listen on port {port}")


    def __str__(self):
        """String representation of the MIDI Listener"""
        return f"<MidiListener: {self._input}, listening on {self.target}>"


    def _callback(self, message):
        """Callback for MidiListener Port"""
        # Add more filters
        if message:
            self.queue.append(message)


    def _get_control(self, control: int, channel: int) -> None:
        """Get a specific control change"""
        if self.queue:
            message=self.queue.pop()
            if (message.type == 'control_change' and message.control == control
               and message.channel == channel):
                    self._last_item = message
            else:
                self._last_item = self._last_item


    def _get_note(self, channel: int) -> None:
        """Get notes from a specific MIDI channel"""
        if self.queue:
            message=self.queue.pop()
            if message.channel == channel:
                    self._last_item = message
            else:
                self._last_item = self._last_item


    def _extract_value(self, message: Union[mido.Message, None]) -> Union[Message, int]:
        """Given a mido.Message, extract needed value based on message type"""

        if message is None:
            return 0

        mtype = message.type
        if mtype == 'control_change':
            value = message.value
        elif mtype in ['note_on', 'note_off']:
            value = message.note
        else:
            return message
        return value


    def get(self):
        """Get an item from the MidiListener"""
        target = self.target

        if isinstance(target, ControlTarget):
            self._get_control(
                    channel=target.channel,
                    control=target.control)
        elif isinstance(target, NoteTarget):
            self._get_note(
                    channel=target.channel)
        else:
            if self.queue:
                self._last_item = self.queue.pop()
            else:
                self._last_item = self._last_item

        return self._extract_value(self._last_item)


    def inspect_queue(self):
        print(f"{self.queue}")


    def kill(self):
        """Close the MIDIListener"""
        self._input.close()


class ClockListener:
    def __init__(
            self,
            port: Optional[str] = None):

        self.queue = deque(maxlen=180)

        if port:
            try:
                self._input = open_input(port)
                self._input.callback = self._callback
                print(f"MidiListener: listening on port {port}")
            except Exception:
                raise OSError(f"Couldn't listen on port {port}")
        else:
            try:
                self._input = open_input()
                self._input.callback = self._callback
                listened_port = mido.get_input_names()[0]
                print(f"MidiListener: listening on port {listened_port}")
            except Exception:
                raise OSError(f"Couldn't listen on port {port}")


    def _callback(self, message):
        """Callback for MidiListener Port"""
        if message.type == 'clock':
            self.queue.append(message)


    def get(self) -> Union[Message, None]:
        """Consume a MIDI Clock Event"""
        if self.queue:
            return self.queue.pop()
        else:
            raise IOError('Empty ClockListener Queue')
