from rich import print
from appdirs import *
from pathlib import Path
import psutil

# gives a single float value
psutil.cpu_percent()
# gives an object with many fields
psutil.virtual_memory()
# you can convert that object to a dictionary 
dict(psutil.virtual_memory()._asdict())
# you can have the percentage of used RAM
psutil.virtual_memory().percent
79.2
# you can calculate percentage of available memory
psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
20.8

APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))


class Logs():

    """
    This class is grouping together several methods used for debugging and
    working on the Clock. My goal is to get sample accurate scheduling
    """

    def __init__(self, clock):
        self._clock = clock

    def clock_drift(self):
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        print(f"Tick dur: {self._clock._get_tick_duration()} " +
              f"CPU: {cpu_usage}%, MEMORY: {memory}%")


    def log(self) -> None:
        """
        Pretty print information about Clock timing on the console.
        Used for debugging purposes. Not to be used when playing,
        can be very verbose. Will overflow the console in no-time.
        """
        cbib = (self._clock.current_beat % self._clock.beat_per_bar) + 1
        bar = self._clock.current_bar

        color = "[bold yellow]"
        first = (
            color + f"BPM: {self._clock.bpm}, PHASE: {self._clock.phase:02}, DELTA: {self._clock._delta:2f}"
        )
        second = color + f" || TICK: {self._clock.tick} BAR:{bar} {cbib}/{self._clock.beat_per_bar}"
        print(first + second)
        print(self.clock_drift())
        if self._clock._link:
            self._clock._link_log()

    def user_path(self):
        print(USER_DIR)

