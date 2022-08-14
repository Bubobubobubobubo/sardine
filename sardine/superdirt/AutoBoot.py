#!/usr/bin/env python3
from os import walk, path
from pathlib import Path
import platform, subprocess, os, signal
import shutil
from typing import Union
from appdirs import *

import psutil
from rich import print

__all__ = ('SuperColliderProcess',)


class SuperColliderProcess:

    """
    Start SCLang process. Allows the execution of SuperCollider
    code directly from the Python side.
    """

    def __init__(self,
            startup_file: Union[str, None] = None,
            preemptive=True):
        appname, appauthor = "Sardine", "Bubobubobubo"
        self._user_dir = Path(user_data_dir(appname, appauthor))
        self._sclang_path = self.find_sclang_path()
        self._synth_directory = self._find_synths_directory()
        self._startup_file = self._find_startup_file(user_file=startup_file)

        if preemptive:
            self.hard_kill()

        self._sclang_proc = subprocess.Popen(
            [self._sclang_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
            start_new_session=True)

        self.boot()


    def _find_vanilla_startup_file(self):
        """ Find the startup file when booting Sardine """
        cur_path = Path(__file__).parent.resolve()
        return "".join([str(cur_path), "/default_superdirt.scd"])


    def _find_startup_file(self, user_file: Union[str, None] = None) -> Path:
        """Find the SuperDirt startup file"""
        if not user_file:
            file_path = Path(
                    '/'.join([str(self._user_dir), "default_superdirt.scd"]))
            if file_path.is_file():
                return file_path
            else:
                # This should definitely be a try/except case
                vanilla_file_path = self._find_vanilla_startup_file()
                shutil.copy(str(vanilla_file_path), self._user_dir)
                return file_path
        else:
            user_file_path = Path(user_file)
            if user_file_path.exists() and user_file_path.is_file():
                return user_file_path
            else:
                # recurse to base case with no user_file
                return self._find_startup_file()


    def _find_synths_directory(self) -> Path:
        """Find or create the synths directory needed"""
        path = Path('/'.join([str(self._user_dir), "synths/"]))
        exists = path.is_dir()
        if exists:
            return path
        else:
            path.mkdir(parents=True)
            return path


    def terminate(self) -> None:
        """Terminate the SCLang process"""

        self.send("Server.killAll; 0.exit;")
        self._sclang_proc.terminate()


    def reset(self) -> None:
        """Restart the SCLang subprocess"""

        self._sclang_proc = subprocess.Popen(
            [self._sclang_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
            start_new_session=True)


    def hard_kill(self) -> None:
        """Look for an instance of SuperCollider, kill it."""

        print("\n[bold red]Preemptive: Killing all SC instances...[/bold red]")
        try:
            for proc in psutil.process_iter():
                if any(procstr in proc.name() for procstr in\
                    ['sclang', 'scide', 'scsynth']):
                    print(f'Killing {proc.name()}')
                    proc.kill()
        except Exception:
            print(f"[yellow]There was no SC process to kill...")


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
        """Open SuperCollider VUmeter"""
        self.send("s.meter()")


    def scope(self) -> None:
        """Open SuperCollider frequency scope"""
        self.send("s.scope()")


    def meterscope(self) -> None:
        """Open SuperCollider frequency scope + VUmeter"""
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
        """Find path to sclang binary, cross-platform"""
        os_name = platform.system()
        if os_name == "Linux":
            return "sclang"
        elif os_name == "Windows":
            if shutil.which("sclang"):
                return "sclang"

            # The Windows installer doesn't usually add sclang to PATH
            # so we'll try to find it manually
            prog = Path(path.expandvars("%programfiles%"))
            colliders = tuple(prog.glob("SuperCollider-*"))
            if not colliders:
                raise OSError("SuperCollider could not be found")

            latest_ish = colliders[-1]
            return str(latest_ish / "sclang.exe")
        elif os_name == "Darwin":
            return "/Applications/SuperCollider.app/Contents/MacOS/sclang"
        else:
            raise OSError('This OS is not officially supported by Sardine.')


    def boot(self) -> None:

        print("\n[red]Starting SCLang && SuperDirt[/red]")
        self.send(message="""load("{}")""".format(self._startup_file))
        # print(f"{self._sclang_proc.communicate()[0]}")
        if self._synth_directory is not None:
            self.load_custom_synthdefs()


    def kill(self) -> None:
        """Kill the connexion with the SC Interpreter"""
        self.send("Server.killAll")
        self.send("0.exit")
