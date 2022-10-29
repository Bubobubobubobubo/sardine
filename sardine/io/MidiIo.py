from typing import Union, TYPE_CHECKING
from rich import print as rich_print
from rich.console import Console
import threading
import asyncio
import mido
import sys

if TYPE_CHECKING:
    from ..clock import Clock

__all__ = ("MIDIIo",)


class MidiNoteEvent:
    def __init__(self, event, due):
        self.event = event
        self.due = due

    def __repr__(self) -> str:
        return f"Due: {self.due}, Event: {self.event}"


class MIDIIo(threading.Thread):
    """
    Direct MIDI I/O Using Mido. MIDI is also available indirectly
    through SuperDirt. I need to do something to address the redun-
    dancy.
    """

    def __init__(
        self,
        clock: "Clock",
        port_name: Union[str, None] = None,
        at: Union[float, int] = 0,
    ):
        """Open a MIDI Output Port. A name can be given, corresponding to
        the name of a valid currently opened MIDI port on the given system.
        If the name is invalid or if the port couldn't be found, the user
        will be faced with a prompt allowing him to select one of the currently
        detected ports.

        Alternatively, if port_name is configured as "Sardine" in the config,
        a new virtual port will spawn, named Sardine.
        """

        threading.Thread.__init__(self)

        self._midi_ports = mido.get_output_names()
        self.port_name = port_name
        self.clock = clock
        self.after: int = at
        self._midi = None
        self._events = {}

        # For MacOS/Linux
        if sys.platform not in "win32":
            if self.port_name in ["Sardine", "internal"]:
                self._midi = mido.open_output("Sardine", virtual=True)
            elif self.port_name:
                self.try_opening_midi_port(name=port_name)
            else:
                self._midi = mido.open_output("Sardine", virtual=True)
        # For W10/W11
        else:
            try:
                self.try_opening_midi_port(name=port_name)
            except Exception as err:
                print(f"[red]Failed to open a MIDI Connexion: {err}")

    def try_opening_midi_port(self, name: str):
        """
        Try to open a MIDI Port. Fallback to _choose_midi_port
        (MIDI Port picker) if provided port name is invalid.
        """
        try:
            self._midi = mido.open_output(name)
        except Exception as error:
            rich_print(f"[bold red]Init error: {error}[/bold red]")
            self._midi = mido.open_output(self._choose_midi_port())

    @staticmethod
    def _choose_midi_port() -> str:
        """ASCII MIDI Port chooser"""
        ports = mido.get_output_names()
        console = Console()
        for (i, item) in enumerate(ports, start=1):
            rich_print(f"[color({i})] {item} [{i}]")
        rich_print(
            "[red]Note: you don't have to hand pick your MIDI Port manually every time."
        )
        rich_print("[red]Check sardine-config to enter a permanent default MIDI port.")
        nb = console.input("[bold yellow] Choose a MIDI Port: [/bold yellow]")
        try:
            nb = int(nb) - 1
            rich_print(f"[yellow]You picked[/yellow] [green]{ports[nb]}[/green].")
            return ports[nb]
        except Exception:
            rich_print(f"Input can only take valid number in range, not {nb}.")
            sys.exit()

    def _process_events(self):
        """MIDI Events to be processed every tick by the clock"""
        to_remove = []
        for key, item in list(self._events.items()):
            item.due -= 1
            if item.due <= 0:
                self.schedule(item.event)
                to_remove.append(key)
        for e in to_remove:
            del self._events[e]

    def send(self, message: mido.Message) -> None:
        self._midi.send(message)

    async def send_async(self, message: mido.Message) -> None:
        self._midi.send(message)

    def send_stop(self) -> None:
        """MIDI Start message"""
        self._midi.send(mido.Message("stop"))

    def send_reset(self) -> None:
        """MIDI Reset message"""
        self._midi.send(mido.Message("reset"))

    def send_clock(self) -> None:
        """MIDI Clock Message"""
        self._midi.send(mido.Message("clock"))

    async def send_start(self, initial: bool = False) -> None:
        """MIDI Start message"""
        self._midi.send(mido.Message("start"))

    def schedule(self, message, delay: Union[int, float, None] = None):
        async def _waiter():
            await handle
            if delay is not None:
                await asyncio.sleep(delay)
            self.send(message)

        ticks = self.clock.get_beat_ticks(self.after, sync=False)
        handle = self.clock.wait_after(n_ticks=ticks)
        asyncio.create_task(_waiter(), name="midi-scheduler")

    async def note(
        self,
        delay: Union[int, float],
        note: int = 60,
        velocity: int = 127,
        channel: int = 1,
    ) -> None:
        """Send a MIDI Note through principal MIDI output"""
        note_id = f"{note}{channel}"
        self._events[note_id + "on"] = MidiNoteEvent(
            due=0,
            event=mido.Message(
                "note_on", note=note, channel=channel, velocity=velocity
            ),
        )
        if note_id + "off" in self._events.keys():
            self.schedule(
                mido.Message("note_off", note=note, channel=channel, velocity=0), 0.0
            )
            self._events[note_id + "off"] = MidiNoteEvent(
                due=delay,
                event=mido.Message("note_off", note=note, channel=channel, velocity=0),
            )
        else:
            self._events[note_id + "off"] = MidiNoteEvent(
                due=delay,
                event=mido.Message("note_off", note=note, channel=channel, velocity=0),
            )

    async def control_change(self, channel, control, value) -> None:
        """Control Change message"""
        self.schedule(
            mido.Message(
                "control_change",
                channel=int(channel),
                control=int(control),
                value=int(value),
            )
        )

    async def program_change(self, channel, program) -> None:
        """Program change message"""
        self.schedule(mido.Message("program_change", program=program, channel=channel))

    async def pitchwheel(self, channel, pitch) -> None:
        """Program change message"""
        self.schedule(mido.Message("pitchweel", pitch=pitch, channel=channel))

    async def sysex(self, data: list[int]) -> None:
        """Custom User Sysex message"""
        self.schedule(mido.Message("sysex", data=bytearray(data), time=0))
