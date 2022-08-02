import mido
import threading
from typing import Union
from rich.console import Console
from rich import print
import asyncio

class MIDIIo(threading.Thread):

    """
    Direct MIDI I/O Using Mido. MIDI is also available indirectly
    through SuperDirt. I need to do something to address the redun-
    dancy.
    """

    def __init__(self, port_name: Union[str, None] = None):
        threading.Thread.__init__(self)
        self._midi_ports = mido.get_output_names()
        if port_name:
            try:
                self._midi = mido.open_output(port_name)
            except Exception as error:
                print(f"[bold red]Init error: {error}[/bold red]")
        else:
            try:
                self._midi = mido.open_output(self.choose_midi_port())
            except Exception as error:
                print(f"[bold red]Init error: {error}[/bold red]")

    def choose_midi_port(self) -> str:
        """ ASCII MIDI Port chooser """
        ports = mido.get_output_names()
        console = Console()
        for (i, item) in enumerate(ports, start=1):
            print(f"[color({i})] [{i}] {item}")
        nb = console.input("[bold yellow] Choose a MIDI Port: [/bold yellow]")
        try:
            nb = int(nb) - 1
            print(f'[yellow]You picked[/yellow] [green]{ports[nb]}[/green].')
            return ports[nb]
        except Exception:
            print(f"Input can only take valid number in range, not {nb}.")
            exit()

    def send(self, message: mido.Message) -> None:
        self._midi.send(message)

    async def send_async(self, message: mido.Message) -> None:
        self._midi.send(message)

    def send_stop(self) -> None:
        """ MIDI Start message """
        self._midi.send(mido.Message('stop'))

    def send_reset(self) -> None:
        """ MIDI Reset message """
        self._midi.send(mido.Message('reset'))
        # self._reset_internal_clock_state()

    def send_clock(self) -> None:
        """ MIDI Clock Message """
        self._midi.send(mido.Message('clock'))

    async def send_clock_async(self) -> None:
        """ MIDI Clock Message """
        self._midi.send(mido.Message('clock'))

    async def send_start(self, initial: bool = False) -> None:
        """ MIDI Start message """
        self._midi.send(mido.Message('start'))

    async def note(self, clock, delay: Union[int, float],
            note:int = 60, velocity: int = 127, channel:int = 1) -> None:
        """ Double message: noteon and noteoff """
        noteon = mido.Message('note_on',
                note=note, velocity=velocity, channel=channel)
        noteoff = mido.Message('note_off',
                note=note, velocity=velocity, channel=channel)

        self._midi.send(noteon)
        duration = clock.tick_time + ((delay * clock.ppqn) - 1)
        while clock.tick_time < duration:
            await asyncio.sleep(clock._get_tick_duration() / clock.ppqn)
        self._midi.send(noteoff)

    def control_change(self, channel, control, value) -> None:
        """ Control Change message """
        self._midi.send(mido.Message('control_change',
            channel=channel, control=control, value=value))
