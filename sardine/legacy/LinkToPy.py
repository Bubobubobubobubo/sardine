from __future__ import print_function
import socket
import edn_format
import os
import numpy as np
import time
import threading
import errno
from socket import error as socket_error
import warnings

__all__ = ("LinkInterface",)


class LinkInterface:
    """A fork of Bdyetton simple python client to communicate with carabiner:
    https://github.com/bdyetton/LinkToPy. Requires edn_format and adapted for
    Sardine."""

    def __init__(
        self,
        path_to_carabiner,
        tcp_ip="127.0.0.1",
        tcp_port=17000,
        buffer_size=1024,
        callbacks=None,
    ):
        self._tcp_ip, self._tcp_port = tcp_ip, tcp_port
        self._buffer_size = buffer_size
        self.peers = 0
        self.quantum_ = 4
        self.phase_ = 0
        self.start_, self.beat_ = [-1] * 2
        self.bpm_ = 120

        if callbacks is None:
            self.callbacks = {}
        else:
            self.callbacks = callbacks

        self.terminated = threading.Event()
        self.start_carabiner_and_open_socket(path_to_carabiner)

        thread = threading.Thread(target=self._listener)
        thread.daemon = True
        thread.start()
        print("Link Interface Started")

    def decode_edn_msg(self, msg):
        """Decodes a TCP message from Carabiner to python dictionary"""
        msg = msg.decode()
        msg_type = msg[: msg.index(" ")]
        try:
            striped_msg = msg[msg.index("{") :]
            decoded_msg = edn_format.loads(striped_msg, write_ply_tables=False)
        except:
            decoded_msg = ""

        # Because the edn_format package does not return normal dam dicts (or string keywords). What dicts.
        if type(decoded_msg) is edn_format.immutable_dict.ImmutableDict:
            decoded_msg = {
                str(key).strip(":"): value for key, value in decoded_msg.dict.items()
            }

        return msg_type, decoded_msg

    def status(self, callback=None):
        """Wrapper for Status"""
        try:
            self.s.send(b"status\n")
        except BrokenPipeError:
            return
        if callback is not None:
            self.callbacks["status"] = callback

    def set_bpm(self, bpm, callback=None):
        """Wrapper for bpm"""
        msg = "bpm " + str(bpm) + "\n"
        try:
            self.s.send(msg.encode())
        except BrokenPipeError:
            return
        if callback is not None:
            self.callbacks["bpm"] = callback

    def beat_at_time(self, time_in_ms, quantum=8, callback=None):
        """Wrapper for Beat At Time"""
        msg = "beat-at-time " + str(time_in_ms) + " " + str(quantum) + "\n"
        try:
            self.s.send(msg.encode())
        except BrokenPipeError:
            return
        if callback is not None:
            self.callbacks["beat-at-time"] = callback

        return

    def time_at_beat(self, beat, quantum=8, callback=None):
        """Wrapper for Time At Beat"""
        msg = "time-at-beat " + str(beat) + " " + str(quantum) + "\n"
        try:
            self.s.send(msg.encode())
        except BrokenPipeError:
            return
        if callback is not None:
            self.callbacks["time-at-beat"] = callback

    def phase_at_time(self, time_in_ms, quantum=8, callback=None):
        """Wrapper for Phase At Time"""
        msg = "phase-at-time " + str(time_in_ms) + " " + str(quantum) + "\n"
        try:
            self.s.send(msg.encode())
        except BrokenPipeError:
            return
        if callback is not None:
            self.callbacks["phase-at-time"] = callback

    def force_beat_at_time(self, beat, time_in_ms, quantum=8, callback=None):
        """Wrapper for Beat At Time"""
        msg = (
            "force-beat-at-time "
            + str(beat)
            + " "
            + str(time_in_ms)
            + " "
            + str(quantum)
            + "\n"
        )
        try:
            self.s.send(msg.encode())
        except BrokenPipeError:
            return
        if callback is not None:
            self.callbacks["force-beat-at-time"] = callback

    def request_beat_at_time(self, beat, time_in_ms, quantum=8, callback=None):
        msg = (
            "request-beat-at-time "
            + str(beat)
            + " "
            + str(time_in_ms)
            + " "
            + str(quantum)
            + "\n"
        )
        try:
            self.s.send(msg.encode())
        except BrokenPipeError:
            return
        if callback is not None:
            self.callbacks["request-beat-at-time"] = callback

    def enable_start_stop_sync(self, callback=None):
        try:
            self.s.send(b"enable-start-stop-sync\n")
        except BrokenPipeError:
            return
        if callback is not None:
            self.callbacks["enable-start-stop-sync"] = callback

    def disable_start_stop_sync(self, callback=None):
        try:
            self.s.send(b"disable-start-stop-sync\n")
        except BrokenPipeError:
            return
        if callback is not None:
            self.callbacks["disable-start-stop-sync"] = callback

    def start_playing(self, time_in_ms, callback=None):
        msg = "start-playing " + str(time_in_ms) + "\n"
        try:
            self.s.send(msg.encode())
        except BrokenPipeError:
            return
        if callback is not None:
            self.callbacks["start-playing"] = callback

    def stop_playing(self, time_in_ms, callback=None):
        msg = "stop-playing " + str(time_in_ms) + "\n"
        try:
            self.s.send(msg.encode())
        except BrokenPipeError:
            return
        if callback is not None:
            self.callbacks["stop-playing"] = callback

    def now(self):
        """Returns the monotonic system time as used by Link. This is in ms, and is the same format as 'start'
        See the Carabiner note on Clocks for more information"""
        return int(time.monotonic() * 1000 * 1000)

    def start_carabiner(self, path_to_car):
        try:
            if os.access(path_to_car, os.X_OK):
                print("Starting Carabiner: %s" % path_to_car)
                pid = os.system(path_to_car + " >car_logs.log")
                self.terminated.clear()

                while True:
                    time.sleep(0.1)
                    try:
                        os.kill(pid, 0)
                    except OSError:
                        break
        except OSError as e:
            print("Couldn't bind with Carabiner: {e}")

            print("Carabiner terminated")
            self.terminated.set()

    def start_carabiner_and_open_socket(self, carabiner_path):
        not_connected, not_connected_ticker = True, 0
        while not_connected:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((self._tcp_ip, self._tcp_port))
                not_connected = False
            except socket_error as serr:
                if serr.errno != errno.ECONNREFUSED:
                    # Not the error we are looking for, re-raise
                    raise serr
                not_connected_ticker += 1

                if not_connected_ticker == 10:
                    thread = threading.Thread(
                        target=self.start_carabiner, args=[carabiner_path]
                    )
                    thread.start()

                if not_connected_ticker > 30:
                    warnings.warn(
                        "Socket Connection Timeout, Carabiner could not be started"
                    )
                    break
                print(".", end='', flush=True)
                time.sleep(0.1)

    def _listener(self):
        while not self.terminated.is_set():
            try:
                msg = self.s.recv(self._buffer_size)
            except BrokenPipeError:
                break

            if msg:
                msg_type, msg_data = self.decode_edn_msg(msg)
            else:
                msg_type = ""

            if msg_type == "beat-at-time":
                self.quantum_ = msg_data["quantum"]

            if msg_type == "phase-at-time":
                self.phase_ = msg_data["phase"]
                self.quantum_ = msg_data["quantum"]

            if msg_type == "status":
                self.bpm_ = msg_data["bpm"]
                self.beat_ = msg_data["beat"]
                self.start_ = msg_data["start"]

            if msg_type == "time_at_beat":
                self.next_beat_ = (msg_data["beat"], msg_data["when"])

            if msg_type in self.callbacks:
                self.callbacks[msg_type](msg_data)

        self.terminated.set()

    def __del__(self):
        self.s.close()
