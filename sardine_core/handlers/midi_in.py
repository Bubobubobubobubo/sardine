import sys
from collections import deque
from dataclasses import dataclass
from typing import Optional

import mido
from mido import Message, get_input_names, open_input, parse_string_stream

from sardine_core.base.handler import BaseHandler
from sardine_core.logger import print

__all__ = ("MidiInHandler",)


def find_midi_in_port(name: str) -> Optional[str]:
    """Find the port name of a MIDI-In port by name."""
    for port in mido.get_input_names():
        port_without_number = port
        if sys.platform == "win32":
            port_without_number = " ".join(port.split(" ")[:-1])
        if name == port_without_number:
            return port
    return None


class MidiInHandler(BaseHandler):
    """
    MIDI-In Listener: listen to incoming MIDI events from a selected port.
    Useful for mapping controllers to control / interact with Sardine.

    The incoming messages are stored in a queue and retrieved in FIFO order.
    """

    def __init__(self, port_name: Optional[str] = None):
        super().__init__()
        self.queues = {}
        self._last_item = {}
        self._last_value = 0

        if port_name:
            port_name = find_midi_in_port(port_name)
            try:
                self._input = open_input(port_name)
                self._input.callback = self._callback
            except Exception:
                error_message = f"Couldn't listen on port {port_name}"
                raise OSError(error_message)
        else:
            try:
                self._input = open_input()
                self._input.callback = self._callback
                listened_port = mido.get_input_names()[0]
            except Exception:
                raise OSError(f"Couldn't listen on port {listened_port}")

    def __str__(self):
        """String representation of the MIDI Listener"""
        return f"<MidiListener: {self._input}>"

    def _get_index_for_control_change(self, control: int, channel: int):
        """Generate a new dictionnary key for each control change route"""
        return f"ctrl:{control},{channel}"

    def _get_index_for_note(self, channel: int):
        """Generate a new dictionnary key for each channel"""
        return f"note:{channel}"

    def _callback(self, message) -> None:
        """Callback for MidiListener Port."""

        def _push_message_to_dict(index: str, message: mido.Message) -> None:
            if index in self.queues:
                self.queues[index].appendleft(message)
            else:
                self.queues[index] = deque(maxlen=20)
                self.queues[index].appendleft(message)

        if message:
            # Case where the message is a control change
            if hasattr(message, "control"):
                queue_dictionnary_index = self._get_index_for_control_change(
                    control=message.control,
                    channel=message.channel,
                )
                if not message.type == "control_change":
                    return
                else:
                    _push_message_to_dict(queue_dictionnary_index, message)
                return
            # Case where the message is a note
            elif hasattr(message, "note"):
                queue_dictionnary_index = self._get_index_for_note(message.channel)
                if not message.type in ("note_off", "note_in"):
                    return
                else:
                    _push_message_to_dict(queue_dictionnary_index, message)
                return
            else:
                # Case where the message is just garbage to dispose of
                return

    def _extract_value(self, message: mido.Message | None) -> Message | int:
        """
        Given a mido.Message, extract needed value based on message type
        """

        if message is None:
            return 0

        mtype = message.type
        if mtype == "control_change":
            value = message.value
        elif mtype in ["note_on", "note_off"]:
            value = message.note
        else:
            return message
        return value

    def _get(self, control: Optional[int], channel: int, last: bool = False):
        """Get an item from the MidiListener event dictionnary. IF last is True,
        return the last element that was inserted and clear the queue. If Control
        is None, then it must be a note"""
        if control:
            idx = self._get_index_for_control_change(control, channel)
        else:
            idx = self._get_index_for_note()
        try:
            queue = self.queues[idx]
        except KeyError:
            return 0

        if queue:
            if last:
                self._last_item[idx] = queue.popleft()
                queue.clear()
            else:
                self._last_item[idx] = queue.pop()

        return self._extract_value(self._last_item[idx])

    def get_control(self, channel: int, control: int, last: bool = False):
        """Get a control change from the MidiListener event dictionnary. If last
        is True, return the last element that was inserted and clear the queue."""
        return self._get(control=control, channel=channel, last=last)

    def get_note(self, channel: int, last: bool = False):
        """Get a note from the MidiListener event dictionnary. If last
        is True, return the last element that was inserted and clear the queue."""
        return self._get(channel=channel, last=last)

    def inspect_queues(self):
        print(f"{self.queues}")

    def kill(self):
        """Close the MIDIListener"""
        self._input.close()
