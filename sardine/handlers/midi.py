from .sender import Number, NumericElement, Sender, ParsableElement
from typing import Optional, Union
from ..utils import alias_param
from ..logger import print
import asyncio
import mido
import sys

__all__ = ("MidiHandler",)


class MidiHandler(Sender):

    """
    MidiHandler: a class capable of reacting to most MIDI Messages.
    """

    def __init__(self, port_name: Optional[str] = None, nudge: float = 0.0):
        super().__init__()
        self.active_notes: dict[tuple[int, int], asyncio.Task] = {}

        # Setting up the MIDI Connexion
        self._available_ports = mido.get_output_names()
        self._port_name = port_name

        # Getting a default MIDI port name
        if port_name in self._available_ports:
            pass
        else:
            if sys.platform in "win32":
                self._port_name = self._available_ports[0]
            else:
                self._port_name = "Sardine"

        self._midi = None

        # For MacOS/Linux
        if sys.platform not in "win32":
            if self._port_name in ["Sardine", "internal"]:
                self._midi = mido.open_output("Sardine", virtual=True)
            else:
                try:
                    self._midi = mido.open_output(self._port_name, virtual=False)
                except Exception as e:  # TODO what error are we trying to catch here?
                    self._midi = mido.open_output(
                        self._available_ports[0], virtual=False
                    )
                    self._port_name = str(self._available_ports[0])

        # For W10/W11
        else:
            try:
                self._midi = mido.open_output(self._port_name)
            except Exception as err:
                print(f"[red]Failed to open a MIDI Connexion: {err}")

        # Setting up the handler
        self._nudge = nudge
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

        # Reference to the ziffers parser if needed!
        self._ziffers_parser = None

    # Ziffers implementation
    @property
    def ziffers_parser(self):
        return self._ziffers_parser

    @ziffers_parser.setter
    def ziffers_parser(self, parser):
        self._ziffers_parser = parser

    def __repr__(self) -> str:
        return f"<{type(self).__name__} port={self._port_name!r} nudge={self._nudge}>"

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

    async def send_off(
        self, note: int, channel: int, velocity: int, delay: Union[int, float]
    ):
        await self.env.sleep(delay)
        self._midi.send(
            mido.Message("note_off", note=note, channel=channel, velocity=velocity)
        )
        self.active_notes.pop((note, channel), None)

    def all_notes_off(self):
        """
        Panic button for MIDI notes on every channel. Is there a message for this?
        """
        for note in range(0, 128):
            for channel in range(0, 16):
                self._midi.send(
                    mido.Message("note_off", note=note, velocity=0, channel=channel)
                )

    def send_midi_note(
        self, note: int, channel: int, velocity: int, duration: float
    ) -> None:
        """
        Function in charge of handling MIDI note sending. This also includes various
        corner cases and typical MIDI note management such as:
        - handling duration by clever combining 'note_on' and 'note_off' events.
        - retriggering: turning a note off and on again if the note is repeated before
          the end of its previously defined duration.
        """

        key = (note, channel)
        note_task = self.active_notes.get(key)

        if note_task is not None and not note_task.done():
            # Brute force solution (temporary fix)
            self._note_off(channel=channel, note=note, velocity=0)
            note_task.cancel()
            self.active_notes.pop(key, None)

        self._midi.send(
            mido.Message(
                "note_on",
                note=int(note),
                channel=int(channel),
                velocity=int(velocity),
            )
        )
        self.active_notes[key] = asyncio.create_task(
            self.send_off(
                note=note, delay=duration - 0.02, velocity=velocity, channel=channel
            )
        )

    @alias_param(name="channel", alias="chan")
    @alias_param(name="duration", alias="dur")
    @alias_param(name="velocity", alias="vel")
    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    def send(
        self,
        note: Optional[NumericElement] = 60,
        velocity: NumericElement = 100,
        channel: NumericElement = 0,
        duration: NumericElement = 1,
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        **rest_of_pattern: ParsableElement,
    ) -> None:
        """
        This method is responsible for preparing the pattern message before sending it
        to the output. This method serves as a template for all other similar 'senders'
        around. It can handle both monophonic and polyphonic messages generated by the
        parser. Any chord will be reduced to a list of dictionaries, transformed again
        into a single MIDI message.
        """

        if note is None:
            return

        if self.apply_conditional_mask_to_bars(
                pattern=rest_of_pattern):
            return

        pattern = {
            "note": note,
            "velocity": velocity,
            "channel": channel,
            "duration": duration,
        }
        deadline = self.env.clock.shifted_time
        for message in self.pattern_reduce(pattern, iterator, divisor, rate):
            if message["note"] is None:
                continue
            for k in ("note", "velocity", "channel"):
                message[k] = int(message[k])
            self.call_timed(deadline, self.send_midi_note, **message)

    @alias_param(name="value", alias="val")
    @alias_param(name="control", alias="ctrl")
    @alias_param(name="channel", alias="chan")
    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    def send_control(
        self,
        control: Optional[NumericElement] = 0,
        channel: NumericElement = 0,
        value: NumericElement = 60,
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        **rest_of_pattern: ParsableElement,
    ) -> None:
        """
        Variant of the 'send' function specialized in sending control changes. See the
        'send' method for more information.
        """

        if control is None:
            return

        if self.apply_conditional_mask_to_bars(
                pattern=rest_of_pattern,
        ):
            return

        pattern = {"control": control, "channel": channel, "value": value}
        deadline = self.env.clock.shifted_time
        for message in self.pattern_reduce(pattern, iterator, divisor, rate):
            if message["control"] is None:
                continue
            for k, v in message.items():
                message[k] = int(v)
            self.call_timed(deadline, self._control_change, **message)

    @alias_param(name="program", alias="prog")
    @alias_param(name="channel", alias="chan")
    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    def send_program(
        self,
        channel: Optional[NumericElement],
        program: NumericElement = 60,
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        **rest_of_pattern: ParsableElement,
    ) -> None:
        if channel is None:
            return

        if self.apply_conditional_mask_to_bars(
                pattern=rest_of_pattern,
        ):
            return

        pattern = {"channel": channel, "program": program}
        deadline = self.env.clock.shifted_time
        for message in self.pattern_reduce(pattern, iterator, divisor, rate):
            if message["channel"] is None:
                continue
            for k, v in message.items():
                message[k] = int(v)
            self.call_timed(deadline, self._program_change, **message)

    @alias_param(name="data", alias="d")
    @alias_param(name="value", alias="v")
    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    def send_sysex(
        self,
        data: list[int],
        value: NumericElement = 60,
        optional_modulo: NumericElement = 127,
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        **rest_of_pattern: ParsableElement,
    ) -> None:
        if data is None:
            return


        if self.apply_conditional_mask_to_bars(
                pattern=rest_of_pattern,
        ):
            return

        pattern = {"value": value}
        deadline = self.env.clock.shifted_time
        for message in self.pattern_reduce(pattern, iterator, divisor, rate):
            if message["value"] is None:
                continue
            for k, v in message.items():
                message[k] = int(v)
            self.call_timed(
                deadline,
                self._sysex,
                **{"data": [*data, *[int(message["value"]) % optional_modulo]]},
            )

    @alias_param(name="channel", alias="chan")
    @alias_param(name="duration", alias="dur")
    @alias_param(name="velocity", alias="vel")
    @alias_param(name="iterator", alias="i")
    @alias_param(name="divisor", alias="d")
    @alias_param(name="rate", alias="r")
    def send_ziffers(
        self,
        ziff: str,
        velocity: NumericElement = 100,
        channel: NumericElement = 0,
        duration: NumericElement = 1,
        iterator: Number = 0,
        divisor: NumericElement = 1,
        rate: NumericElement = 1,
        scale: str = "IONIAN",
        key: str = "C4",
        **rest_of_pattern: ParsableElement,
    ) -> int | float:
        """
        Alternative to the send method for the ziffers sender. The message will be pre-
        pared and mixed with the result of a ziffers message!
        """

        if self.apply_conditional_mask_to_bars(
                pattern=rest_of_pattern,
        ):
            return

        if not self._ziffers_parser:
            raise Exception("The ziffers package is not imported!")
        else:
            # Getting the ziffer pattern
            ziffer = self._ziffers_parser(ziff, scale=scale, key=key)[iterator]
            try:
                note = ziffer.note
            except AttributeError:  # if there is no note, it must be a silence
                try:
                    note = ziffer.notes
                except AttributeError:
                    note = "."

            if isinstance(note, list):
                note = f"{{{', '.join([str(x) for x in note])}}}"

        pattern = {
            "note": note,
            "velocity": velocity,
            "channel": channel,
            "duration": duration,
        }

        deadline = self.env.clock.shifted_time

        for message in self.pattern_reduce(pattern, iterator, divisor, rate):
            if message["note"] is None:
                continue
            for k in ("note", "velocity", "channel"):
                message[k] = int(message[k])
            self.call_timed(deadline, self.send_midi_note, **message)

        return ziffer.duration * (self.env.clock.beats_per_bar)
