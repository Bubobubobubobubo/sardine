from typing import Callable, Union
from rich.panel import Panel
from rich import print

__all__ = ("Player",)

class Player:

    """
    A Player is a lone Sender that will be activated by a central surfing
    swimming function. It contains the sender and basic information about
    div, rate, etc...
    """

    def __init__(self, name: str, content: Union[None, dict] = {}):
        self._name = name
        self._content = content

    @classmethod
    def run(cls, func: Callable):
        """
        The run method can be used to schedule any arbitrary function in rhythm just
        like if it was a regular swimming function with a lone function call nested 
        inside it.
        """
        return {"type": "function", "func": func}

    @classmethod
    def play(cls, *args, **kwargs):
        """
        The play method is analog to using the 'D()' send method (SuperDirt).
        """
        return {"type": "sound", "args": args, "kwargs": kwargs}

    @classmethod
    def play_midi(cls, *args, **kwargs):
        """
        The play_midi method is analog to using the 'M()' send method (MIDIOut).
        """
        return {"type": "MIDI", "args": args, "kwargs": kwargs}

    @classmethod
    def play_control(cls, *args, **kwargs):
        """
        The play_control method is analog to using the 'CC()' send method (CCSender).
        """
        return {"type": "MIDI", "args": args, "kwargs": kwargs}

    @classmethod
    def play_osc(cls, *args, **kwargs):
        """
        #TODO: what to do of this?
        """
        return {"type": "OSC", "args": args, "kwargs": kwargs}

    def __rshift__(self, method_result):
        """
        Entry point for allocating a task to a given Player. Possible tasks are 'play',
        'play_midi', 'play_osc', 'play_control' or 'run'. These methods all correspond 
        to one possible simple operation to pattern and more could be added in the 
        future.
        """
        print(Panel.fit(f"[yellow][[red]{self._name}[/red] update!][/yellow]"))
        self._content = method_result

    def __repr__(self) -> str:
        return f"[Player {self._name}]: {self._content}, div: {self._div}, rate: {self._rate}"
