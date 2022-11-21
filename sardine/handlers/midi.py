import sys
import threading

import mido

from ..base.handler import BaseHandler
from ..io.MidiIo import MIDIIo
from typing import Union, Optional, TYPE_CHECKING
from itertools import cycle
from ..sequences import Chord

__all__ = ("MidiHandler",)


class MidiHandler(BaseHandler, threading.Thread):

    """
    MidiHandler: a class capable of reacting to most MIDI Messages.
    """

    def __init__(self, port_name: str = "Sardine"):
        # Not exactly a pleasing solution for multiple inheritance
        threading.Thread.__init__(self)
        BaseHandler.__init__(self)
        self.active_notes: dict[tuple[int, int], asyncio.Task] = {}


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

        # Setting up the handler
        self.env = None
        self.events = {
            "start": self._start,
            "continue": self._continue,
            "stop": self._stop,
            "reset": self._reset,
            "clock": self._clock,
            "note_on": self._note_on,
            "note_off": self._note_off,
            "aftertouch": self._aftertouch,
            "polytouch": self._polytouch,
            "control_change": self._control_change,
            "program_change": self._program_change,
            "sysex": self._sysex,
            "pitchwheel": self._pitch_wheel,
        }

    def __repr__(self) -> str:
        return f"{self._port_name}: MIDI Handler"

    def setup(self):
        for event in self.events:
            self.register(event)

    def hook(self, event: str, *args):
        func = self.events[event]
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
        self._midi.send(
            mido.Message("note_on", channel=channel, note=note, velocity=velocity)
        )

    def _note_off(self, channel: int, note: int, velocity: int) -> None:
        self._midi.send(
            mido.Message("note_off", channel=channel, note=note, velocity=velocity)
        )

    def _polytouch(self, channel: int, note: int, value: int) -> None:
        self._midi.send(
            mido.Message("polytouch", channel=channel, note=note, value=value)
        )

    def _aftertouch(self, channel: int, value: int) -> None:
        self._midi.send(mido.Message("aftertouch", channel=channel, value=value))

    def _control_change(self, channel: int, control: int, value: int) -> None:
        self._midi.send(
            mido.Message(
                "control_change", channel=channel, control=control, value=value
            )
        )

    def _program_change(self, program: int, channel: int) -> None:
        self._midi.send(
            mido.Message("program_change", program=program, channel=channel)
        )

    def _sysex(self, data: bytearray, time: int = 0) -> None:
        self._midi.send(mido.Message("sysex", data=data, time=time))

    def _pitch_wheel(self, pitch: int, channel: int) -> None:
        self._midi.send(mido.Message("pitchweel", pitch=pitch, channel=channel))

    async def send_off(self, delay: float, note: int, channel: int):
        await self.env.sleep(delay)
        self.push("note_off", note, channel)
        self.active_notes.pop((note, channel), None)

    def _clamp(n: int, minimum: int, maximum: int): 
        """Simple clamping function"""
        return max(minimum, min(n, maximum))

    def send_control(
        self, 
        channel: Union[str, int],
        control: Union[str, int],
        value: Union[str, int],
        d: Optional[Union[str, int]] = 1,
        r: Optional[Union[str, int]] = 1,
        i: int = 1) -> None:
        """Out function for CC Messages"""

        # 0) Gathering arguments
        iterator, divisor, rate = (i, d, r)
        patterns = {
            k:parse(v) if isinstance(v, str) else v for k, v in 
            {
                'channel': channel, 'control': control, 'value': value,
                'iterator': iterator, 'divisor': divisor, 'rate': rate
            }.items()
        }

    def send(
        self,
        note: Union[str, int] = 60,
        velocity: Union[str, int] = 100,
        channel: Union[str, int] = 0,
        duration: Union[str, int] = 1,
        iterator: Optional[Union[str, int]] = 1,
        d: Optional[Union[str, int]] = 1,
        r: Optional[Union[str, int]] = 1,
        i: int = 1) -> None:
        """Out function for MIDI Notes"""
        parse = self.env.parser.parse

        def send_midi_note(
            note: int, 
            channel: int,
            velocity: int,
            duration: float, 
        ) -> None:
            """Template function for MIDI Note sending (in a threading context)"""
            key = (note, channel)

            note_task = self.active_notes.get(key)
            if note_task is not None:
                note_task.cancel()
            else:
                self.push("note_on", note, channel, velocity, ...)

            self.active_notes[key] = asyncio.create_task(
                self.send_off(duration, note, channel, velocity)
            )

        def chords_in_pattern(pattern: dict) -> bool:
            """Check for the presence of chords in any given pattern"""
            patterns = pattern.values()
            for pattern in patterns:
                for element in pattern:
                    if isinstance(element, Chord):
                        return True
                    else:
                        pass
            return False

            #return any(isinstance(x, Chord) for x in pattern.values())

        def longest_list_in_pattern(pattern: dict) -> int:
            return max(len(x) if isinstance(x, (Chord, list)) else 1 for x in pattern.values())

        # 0) Gathering arguments
        iterator, divisor, rate = (i, d, r)
        patterns = {
            k:parse(v) if isinstance(v, str) else v for k, v in 
            {
                'note': note, 'velocity': velocity,
                'channel': channel, 'duration': duration,
                'iterator': iterator, 'divisor': divisor,
                'rate': rate
            }.items()
        }
        if iterator % (divisor[iterator] if isinstance(divisor, list) else divisor) != 0:
            return

        # 2) Composing a message (caring for monophonic and/or polyphonic messages)

        # Dealing with polyphonic messages
        if chords_in_pattern(patterns):
            message_list = []
            longest_message = longest_list_in_pattern(patterns)
            for key in patterns.keys():
                if isinstance(patterns[key], int):
                    patterns[key] = cycle([patterns[key]])
                elif isinstance(patterns[key], (list)):
                    if isinstance(patterns[key][0], Chord):
                        patterns[key] = cycle(list(patterns[key][0]))
                    else:
                        patterns[key] = cycle(patterns[key])
            for _ in range(longest_message):
                message_list.append({k:next(v) for k, v in patterns.items()})

            # The logic is broken as hell...
            for messages in message_list:
                send_midi_note(
                    note= messages['note'][divisor] if isinstance(note, list) else note,
                    channel= messages['channel'][divisor] if isinstance(channel, list) else channel,
                    velocity= messages['velocity'][divisor] if isinstance(velocity, list) else velocity,
                    duration= messages['duration'][divisor] if isinstance(duration, list) else duration,
                )

        # Dealing with monophonic messages
        else:
            send_midi_note(
                note= note[divisor] if isinstance(note, list) else note,
                channel= channel[divisor] if isinstance(channel, list) else channel,
                velocity= velocity[divisor] if isinstance(velocity, list) else velocity,
                duration= duration[divisor] if isinstance(duration, list) else duration,
            )


        # 3) Dispatching
