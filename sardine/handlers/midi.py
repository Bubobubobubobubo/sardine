import sys
import asyncio
import threading

import mido

from ..base.handler import BaseHandler
from typing import Union
from rich import print
from math import floor
from ..sequences import Chord
from functools import wraps

__all__ = ("MidiHandler",)

VALUES = Union[int, float, list, str]
PATTERN = dict[str, list[float | int | list | str]]
REDUCED_PATTERN = dict[str, list[float | int]]


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

    async def send_off(self, note: int, channel: int, velocity: int, delay: Union[int, float]):
        await self.env.sleep(delay)
        self._midi.send(mido.Message("note_off", note=note, 
            channel=channel, velocity=velocity))
        self.active_notes.pop((note, channel), None)

    def all_notes_off(self):
        """
        Panic button for MIDI notes on every channel. Is there a message for this?
        """
        for note in range(0,128):
            for channel in range(0,16):
                self._midi.send(mido.Message(
                    'note_off',
                    note=note,velocity=0,
                    channel=channel))

    def send_midi_note(self,
            note: int,
            channel: int,
            velocity: int,
            duration: float
    ) -> None:
        """Template function for MIDI Note sending"""

        key = (note, channel)
        note_task = self.active_notes.get(key)
        if note_task is not None and not note_task.done():
            note_task.cancel()
        else:
            self._midi.send(mido.Message(
                'note_on', note=int(note), channel=int(channel),
                velocity=int(velocity)))
            self.active_notes[key] = asyncio.create_task(
                self.send_off(note=note, delay=duration-0.02,
                    velocity=velocity, channel=channel))


    def pattern_element(self, div: int, rate: int, iterator: int, pattern: list) -> int:
        """Joseph Enguehard's algorithm for solving iteration speed"""
        return floor(iterator * rate / div) % len(pattern)

    
    def pattern_reduce(self, 
            pattern: PATTERN, 
            iterator: int, 
            divisor: int, 
            rate: float,
            break_polyphony=False,
    ) -> dict:
        pattern = {
                k: self.env.parser.parse(v) if isinstance(
            v, str) else v for k, v in pattern.items()
        }
        pattern = {
                k:v[self.pattern_element(
                    div=divisor, 
                    rate=rate, 
                    iterator=iterator,
                    pattern=v)] if hasattr(
                        v, "__getitem__") else v for k, v in pattern.items()
        }
        return pattern

    def reduce_polyphonic_message(
            self,
            pattern: PATTERN) -> list[dict]:
        """
        Reduce a polyphonic message to a list of messages represented as 
        dictionaries holding values to be sent through the MIDI Port
        """
        message_list: list = []
        length = [x for x in filter(
            lambda x: hasattr(x, '__getitem__'), pattern.values())
        ]
        length = max([len(i) for i in length])

        # Break the chords into lists
        pattern = {k:list(value) if isinstance(
            value, Chord) else value for k, value in pattern.items()}

        for _ in range(length):
            message_list.append({k:v[_%len(v)] if isinstance(
                v, (Chord, list)) else v for k, v in pattern.items()}
            )
        return message_list

    @staticmethod
    def _alias_param(name, alias):
        """
        Alias a keyword parameter in a function. Throws a TypeError when a value is
        given for both the original kwarg and the alias. Method taken from 
        github.com/thegamecracks/abattlemetrics/blob/main/abattlemetrics/client.py
        (@thegamecracks).
        """
        MISSING = object()
    
        def deco(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                alias_value = kwargs.pop(alias, MISSING)
                if alias_value is not MISSING:
                    if name in kwargs:
                        raise TypeError(f'Cannot pass both {name!r} and {alias!r} in call')
                    kwargs[name] = alias_value
                return func(*args, **kwargs)
            return wrapper
        return deco

    @_alias_param(name='iterator', alias='i')
    @_alias_param(name='divisor', alias='d')
    @_alias_param(name='rate', alias='r')
    def send(
        self,
        note: VALUES = 60, 
        velocity: VALUES = 100,
        channel: VALUES = 0, 
        duration: VALUES = 1,
        iterator: int = 0, 
        divisor: int = 1,
        rate: float = 1
    ) -> None:
        """
        This method is responsible for preparing the pattern message before sending it 
        to the output. This method serves as a template for all other similar 'senders'
        around. It can handle both monophonic and polyphonic messages generated by the
        parser. Any chord will be reduced to a list of dictionaries, transformed again
        into a single MIDI message.
        """

        if iterator % divisor!= 0: 
            return

        pattern = self.pattern_reduce(
                break_polyphony=False,
                pattern={
                    'note': note,
                    'velocity': velocity, 
                    'channel': channel, 
                    'duration': duration
                },
                iterator=iterator, 
                divisor=divisor, 
                rate=rate 
        )

        is_polyphonic = any(isinstance(v, Chord) for v in pattern.values())

        if is_polyphonic:
            for message in self.reduce_polyphonic_message(pattern):
                if not isinstance(message['note'], type(None)):
                    self.send_midi_note(
                            note=message['note'], 
                            channel=message['channel'], 
                            velocity=message['velocity'], 
                            duration=message['duration']
                    )
        else:
            if not isinstance(pattern['note'], type(None)):
                self.send_midi_note(
                        note=pattern['note'],
                        channel=pattern['channel'],
                        velocity=pattern['velocity'],
                        duration=pattern['duration']
                )

    @_alias_param(name='iterator', alias='i')
    @_alias_param(name='divisor', alias='d')
    @_alias_param(name='rate', alias='r')
    def send_control(
        self,
        control: VALUES = 0, 
        channel: VALUES = 0,
        value: VALUES = 60,
        iterator: int = 0, 
        divisor: int = 1,
        rate: float = 1
    ) -> None:
        """
        Variant of the 'send' function specialized in sending control changes. See the
        'send' method for more information. 
        """

        if iterator % divisor!= 0: 
            return

        pattern = self.pattern_reduce(
                break_polyphony=False,
                pattern={
                    'control': control,
                    'channel': channel, 
                    'value': value, 
                },
                iterator=iterator, 
                divisor=divisor, 
                rate=rate 
        )

        is_polyphonic = any(isinstance(v, Chord) for v in pattern.values())

        if is_polyphonic:
            for message in self.reduce_polyphonic_message(pattern):
                if not isinstance(message['control'], type(None)):
                    self._control_change(
                    control=int(message['control']),
                    channel=int(message['channel']),
                    value=int(message['value']))
        else:
            if not isinstance(pattern['control'], type(None)):
                self._control_change(
                    control=int(pattern['control']),
                    channel=int(pattern['channel']),
                    value=int(pattern['value']))

    @_alias_param(name='iterator', alias='i')
    @_alias_param(name='divisor', alias='d')
    @_alias_param(name='rate', alias='r')
    def send_program(
        self,
        channel: VALUES,
        value: VALUES = 60,
        iterator: int = 0, 
        divisor: int = 1,
        rate: float = 1
    ) -> None:
        if iterator % divisor!= 0: 
            return

        pattern = self.pattern_reduce(
                break_polyphony=False,
                pattern={
                    'channel': channel,
                    'value': value, 
                },
                iterator=iterator, 
                divisor=divisor, 
                rate=rate 
        )

        is_polyphonic = any(isinstance(v, Chord) for v in pattern.values())

        if is_polyphonic:
            for message in self.reduce_polyphonic_message(pattern):
                if not isinstance(message['channel'], type(None)):
                    self._program_change(
                            program=message['value'], 
                            channel=message['channel']
                    )
        else:
            if not isinstance(pattern['channel'], type(None)):
                self._program_change(
                        program=pattern['value'], 
                        channel=pattern['channel']
                )

