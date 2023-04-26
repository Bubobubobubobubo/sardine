from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import osc_send, osc_udp_client
from abc import ABC
from typing import Dict, Any

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

    def notify_tick(self, cycle, s, cps, bpc, mill, now):
        """Called by a Clock every time it ticks, when subscribed to it"""
        if not self.pattern:
            return

        cycle_from, cycle_to = cycle
        es = self.pattern.onsets_only().query(TimeSpan(cycle_from, cycle_to))
        if len(es):
            _logger.debug("%s", [e.value for e in es])

        for e in es:
            cycle_on = e.whole.begin
            cycle_off = e.whole.end

            link_on = s.timeAtBeat(cycle_on * bpc, 0)
            link_off = s.timeAtBeat(cycle_off * bpc, 0)
            delta_secs = (link_off - link_on) / mill

            # TODO: fix for osc4py3
            # link_secs = now / mill
            # liblo_diff = liblo.time() - link_secs
            # nudge = e.value.get("nudge", 0)
            # ts = (link_on / mill) + liblo_diff + self.latency + nudge

            self.notify_event(
                e.value,
                timestamp=ts,
                cps=float(cps),
                cycle=float(cycle_on),
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


class SuperDirtStream(BaseStream):
    """
    This Stream class sends control pattern messages to SuperDirt via OSC

    Parameters
    ----------
    port: int
        The port where SuperDirt is listening
    latency: float
        SuperDirt latency

    """

    def __init__(self, port=57120, latency=0.2, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.latency = latency
        self.name = "vortex"

        self._port = port
        self._address = "127.0.0.1"

        self.osc_client = osc_udp_client(
                address="127.0.0.1", 
                port=57120,
                name=self.name
        )


    @property
    def port(self):
        """SuperDirt listening port"""
        return self._port

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
        _logger.info("%s", msg)

        # TODO: make a bundle using osc4py3
        # liblo.send(superdirt, "/dirt/play", *msg)
        # bundle = liblo.Bundle(timestamp, liblo.Message("/dirt/play", *msg))
        # liblo.send(self._address, bundle)

