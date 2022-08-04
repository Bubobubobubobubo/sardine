#!/usr/bin/env python3
from time import time
from typing import Union

from osc4py3 import oscbuildparse
from osc4py3.as_eventloop import (
    osc_startup, osc_udp_client, osc_send, osc_process
)

__all__ = ('Client', 'client', 'dirt')


class Client:

    def __init__(self, ip: str = "127.0.0.1",
                 port: int = 57120, name: str = "SuperDirt",
                 ahead_amount: Union[float, int] = 0.5):

        """
        Keyword parameters
        ip: str -- IP
        port: int -- network port
        name: str -- Name attributed to the OSC connexion
        ahead_amount: Union[float, int] -- (in ms.) send timestamp
                      in the future, x ms. after current time.
        """

        self._ip, self._port = (ip, port)
        self._name, self._ahead_amount = (name, ahead_amount)
        osc_startup()
        osc_udp_client(
                address=self._ip,
                port=self._port,
                name=self._name)

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value

    @property
    def ahead_amount(self):
        return self._ahead_amount

    @ahead_amount.setter
    def ahead_amount(self, value):
        self._ahead_amount = value

    def send(self, address: str, message):
        """ Build user-made OSC messages """
        msg = oscbuildparse.OSCMessage(address, None, message)
        bun = oscbuildparse.OSCBundle(
            oscbuildparse.unixtime2timetag(time() + self._ahead_amount), [msg])
        osc_send(bun, self._name)
        osc_process()

    def send_timed_message(self, message):
        """ Build and send OSC bundles """
        msg = oscbuildparse.OSCMessage("/play2", None, message)
        bun = oscbuildparse.OSCBundle(
            oscbuildparse.unixtime2timetag(time() + self._ahead_amount), [msg])
        osc_send(bun, self._name)
        osc_process()


client = Client()


def dirt(message):
    """ Sending messages to SuperDirt/SuperCollider """
    client.send_timed_message(message)
