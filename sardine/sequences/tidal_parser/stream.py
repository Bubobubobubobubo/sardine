from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import osc_send, osc_udp_client
from abc import ABC
from typing import Dict, Any, Optional
from .pattern import *
from time import time


class BaseStream(ABC):
    """
    A class for playing control pattern events

    It should be subscribed to a LinkClock instance.

    Parameters
    ----------
    name: Optional[str]
        Name of the stream instance

    """

    def __init__(self, name: str = None):
        self.name = name
        self.pattern = None

    def notify_tick(
        self,
        clock,
        cycle: tuple,
        cycles_per_second: float,
        beats_per_cycle: int,
        now: int | float,
    ):
        """Called by a Clock every time it ticks, when subscribed to it"""
        if not self.pattern:
            return

        # Querying the pattern using time information
        cycle_from, cycle_to = cycle
        es = self.pattern.onsets_only().query(TimeSpan(cycle_from, cycle_to))

        # Processing individual events
        for e in es:
            cycle_on, cycle_off = e.whole.begin, e.whole.end
            on = clock.timeAtBeat(cycle_on * beats_per_cycle)
            off = clock.timeAtBeat(cycle_off * beats_per_cycle)
            delta_secs = (off - on)

            link_secs = clock.shifted_time + clock._tidal_nudge
            nudge = e.value.get("nudge", 0)
            ts = (on) + self.latency + nudge

            self.notify_event(
                e.value,
                timestamp=ts,
                cps=float(cycles_per_second),
                cycle=float(on),
                delta=float(delta_secs),
            )

    def notify_event(
        self,
        event: Dict[str, Any],
        timestamp: float,
        cps: float,
        cycle: float,
        delta: float,
    ):
        """Called by `notify_tick` with the event and timestamp that should be played"""
        raise NotImplementedError

    def __repr__(self):
        pattern_repr = " \n" + repr(self.pattern) if self.pattern else ""
        return f"<{self.__class__.__name__} {repr(self.name)}{pattern_repr}>"


class TidalStream(BaseStream):

    def __init__(self, osc_client, latency=0.0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.latency = latency
        self.name = "vortex"
        self._osc_client = osc_client
        self._last_value: Optional[dict] = None

    def get(self) -> Any:
        """Return a dictionary of the last message played by the stream"""
        return self._last_value

    def notify_event(
        self,
        event: Dict[str, Any],
        timestamp: float,
        cps: float,
        cycle: float,
        delta: float,
    ):
        msg = []
        for key, val in event.items():
            if isinstance(val, Fraction):
                val = float(val)
            msg.append(key)
            msg.append(val)
        msg.extend(["cps", cps, "cycle", cycle, "delta", delta])

        self._last_value = dict(zip(msg[::2], msg[1::2]))
        self._osc_client._send_timed_message(address="/dirt/play", message=msg)
