#!/usr/bin/env python3
from os import walk
import pathlib
import platform, threading, subprocess, os, signal
from time import sleep
from typing import Union

from rich import print

__all__ = ('find_startup_file', 'find_synth_directory', 'SuperColliderProcess')


def find_startup_file():
    """ Find the startup file when booting Sardine """
    cur_path = pathlib.Path(__file__).parent.resolve()
    return "".join([str(cur_path), "/configuration/startup.scd"])

def find_synth_directory():
    """ Find the synth directory when booting Sardine """
    cur_path = pathlib.Path(__file__).parent.resolve()
    return "".join([str(cur_path), "/configuration/synths/"])


class SuperColliderProcess():

    """
    Start SCLang process. Allows the execution of SuperCollider
    code directly from the Python side.
    """

    def __init__(self,
            synth_directory: Union[str, None],
            startup_file: str):

        self._sclang_path = self.find_sclang_path()
        self._synth_directory = synth_directory
        self._startup_file = startup_file
        self._sclang_proc = subprocess.Popen(
            [self._sclang_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
            start_new_session=True)


    def terminate(self) -> None:

        """
        Terminate the SCLang process
        """

        self.send("Server.killAll;")
        self.send("0.exit")
        # self._proc_thread.join()
        self._sclang_proc.terminate()

    def reset(self) -> None:

        """
        Restart the SCLang process
        """

        self._sclang_proc = subprocess.Popen(
            [self._sclang_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
            start_new_session=True)

    def hard_reset(self) -> None:

        """
        Search all running instances of sclang, scsynth and scide.
        Kill all existing running processes.
        """

        print("[bold red] Killing SC internal process...[/bold red]")
        self.terminate()
        print("[bold red] Killing all SC instances...[/bold red]")
        for sc_process in ["scsynth", "sclang", "scide"]:
            for line in os.popen(f"ps ax | grep {sc_process} | grep -v grep"):
                fields = line.split()
                os.kill(int(fields[0]),
                        signal.SIGKILL)
        self.reset()

    def send(self, message: str):

        """
        Pipe strings to SCLang: message: single or multi-line string.
        TODO: Fix multiline support.
        """

        # Converting messages for multiline-input
        message = "".join(message.splitlines())

        # Linebreak for the last line..
        if not message.endswith('\n'): message += '\n'

        # Writing messages
        self._sclang_proc.stdin.write(message)
        self._sclang_proc.stdin.flush()

    def meter(self) -> None:
        """ Open SuperCollider mixer view """
        self.send("s.meter()")

    def scope(self) -> None:
        """ Open SuperCollider stethoscope """
        self.send("s.scope()")

    def meterscope(self) -> None:
        """ Open SuperCollider sthethoscope + mixer """
        self.send("s.scope(); s.meter()")

    def check_synth_file_extension(self, string: str) -> bool:
        return string.endswith(".scd") or string.endswith(".sc")

    def startup_file_path(self) -> str:
        return self._startup_file

    def load_custom_synthdefs(self) -> None:
        buffer = ""
        _, _, files = next(walk(self._synth_directory))

        # Filter by file extension (only .sc and .scd)
        files = [f for f in files if self.check_synth_file_extension(f)]
        if len(files) > 0:
            for fname in files:
                with open(self._synth_directory + "/" + fname) as infile:
                    for line in infile:
                        buffer += line

            # sending the string to the interpreter
            self.send(buffer)
            print("Loaded SynthDefs:")
            for f in files:
                print("- {}".format(f))

    def find_sclang_path(self) -> str:

        """
        Finding path to the SCLang CLI on every major platform.
        """
        os = platform.system()
        if os == "Linux":
            return "sclang"
        elif os == "Windows":
            return "scsynth.exe"
        elif os == "Darwin":
            return "/Applications/SuperCollider.app/Contents/MacOS/sclang"
        else:
            # Probably better to raise an exception here
            return ""

    async def boot(self) -> None:

        print("[red]Starting SCLang[/red]")
        self.send(message="""load("{}")""".format(self._startup_file))
        sleep(1)
        if self._synth_directory is not None:
            self.load_custom_synthdefs()

    def kill(self) -> None:
        """ Kill the connexion with the SC Interpreter """
        self.send("Server.killAll")
        sleep(1)
        self.send("0.exit")
