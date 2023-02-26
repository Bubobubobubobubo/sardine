#!/usr/bin/env python3
import asyncio
import platform
import shutil
import subprocess
import tempfile
from os import path, walk
from pathlib import Path
from typing import Optional, Union

import psutil
from appdirs import *
from ..logger import print
from rich.console import Console

__all__ = ("SuperDirtProcess",)


class SuperDirtProcess:
    def __init__(
        self, startup_file: Optional[str] = None, preemptive=True, verbose=False
    ):

        appname, appauthor = "Sardine", "Bubobubobubo"
        self._user_dir = Path(user_data_dir(appname, appauthor))
        self._sclang_path = self.find_sclang_path()
        self._synth_directory = self._find_synths_directory()
        self._startup_file = (
            self._find_startup_file(user_file=startup_file)
            if startup_file is not None
            else None
        )
        self.temp_file = tempfile.NamedTemporaryFile()
        self._verbose = verbose

        # If preemptive, all previously running instances of SuperCollider
        # will be killed to prevent more issues...
        if preemptive:
            self.hard_kill()

        self.boot()

        asyncio.create_task(self.monitor())

    def _find_vanilla_startup_file(self):
        """Find the startup file when booting Sardine"""
        cur_path = Path(__file__).parent.resolve()
        return "".join([str(cur_path), "/default_superdirt.scd"])

    def _find_startup_file(self, user_file: Union[str, None] = None) -> Path:
        """Find the SuperDirt startup file"""
        if not user_file:
            file_path = self._user_dir / "default_superdirt.scd"
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
        path = self._user_dir / "synths/"
        exists = path.is_dir()
        if exists:
            return path
        else:
            path.mkdir(parents=True)
            return path

    def terminate(self) -> None:
        """Terminate the SCLang process"""
        self._write_stdin("Server.killAll; 0.exit;")
        self._sclang.terminate()

    def _analyze_and_warn(self, decoded_line: str):
        """
        Analyse the last line from SuperCollider logs and warn the user if something
        shady is going on (like not being able to boot the server, late messages)
        """
        if "no synth or sample" in decoded_line:
            sample_name = decoded_line.split("'")
            print(f"[[red]/!\\\\[/red] - Sample {sample_name[1]} not found]")
        if "late 0." in decoded_line:
            print(f"[[red]/!\\\\[/red] - Late messages. Increase SC latency]")
        if "listening to Tidal on port 57120" in decoded_line:
            print(f"[[green]/!\\\\[/green] - Audio server ready!]")
            if self._synth_directory is not None:
                self.load_custom_synthdefs()
        if "ERROR: failed to open UDP socket: address in use" in decoded_line:
            print("\n")
            print(
                    (
                        f"[red]/!\\\\[/red] - Socket in use! SuperCollider is already"
                        + "\nrunning somewhere. It might be a mistake or a"
                        + "\nzombie process. Run `Server.killAll` in an SC"
                        + "\nwindow (can be the IDE of `sclang` in term..)"
                    )
            )
        if "Mismatched sample rates are not supported" in decoded_line:
            print("\n")
            print(
                    (
                        f"[red]/!\\\\[/red] - Mismatched sample rates. Please make"
                        + "\nsure that your audio input sample rate and"
                        + "\nyour audio output sample rate are the same."
                        + "\nThis is usually modified in your OS audio"
                        + "\nconfiguration menus. Reboot Sardine!"
                    )
            )

    async def monitor(self):
        """
        Monitoring SuperCollider output using an asynchronous function
        that runs on a loop and prints to output. Can be quite verbose at
        boot time!
        """
        import sys

        try:
            while self._sclang.poll() is None:
                where = self.temp_file.tell()
                lines = self.temp_file.read()
                if not lines:
                    await asyncio.sleep(0.1)
                    self.temp_file.seek(where)
                else:
                    if self._verbose:
                        sys.__stdout__.write(lines.decode())
                    else:
                        self._analyze_and_warn(lines.decode())
                    sys.__stdout__.flush()
            sys.__stdout__.write(self.temp_file.read())
            sys.__stdout__.flush()
        except UnboundLocalError:
            raise UnboundLocalError("SCLang is not reachable...")

    def hard_kill(self) -> None:
        """Look for all instances of SuperCollider, kill them."""
        try:
            for proc in psutil.process_iter():
                if any(
                    procstr in proc.name() for procstr in ["sclang", "scide", "scsynth"]
                ):
                    proc.kill()
        except Exception:
            pass

    def _write_stdin(self, message: str):
        """Write to sclang stdin using Python strings"""

        # Converting messages for multiline-input
        message = "".join(message.splitlines())

        # Linebreak for the last line..
        if not message.endswith("\n"):
            message += "\n"

        # Writing messages (TODO: fix mechanism)
        self._sclang.stdin.write(message)
        self._sclang.stdin.flush()

    def send(self, message: str):
        """User friendly alias for write_stdin"""
        self._write_stdin(message)

    def trace(self, value: bool = True) -> None:
        """Tracing OSC messages sent to SuperCollider (only visible in verbose mode)"""
        self._write_stdin(f"OSCFunc.trace({'true' if value else 'false'});")

    def meter(self) -> None:
        """Open SuperCollider VUmeter"""
        self._write_stdin("s.meter()")

    def scope(self) -> None:
        """Open SuperCollider frequency scope"""
        self._write_stdin("s.scope()")

    def freqscope(self) -> None:
        """Open SuperCollider frequency scope"""
        self._write_stdin("s.freqscope()")

    def meterscope(self) -> None:
        """Open SuperCollider frequency scope + VUmeter"""
        self._write_stdin("s.scope(); s.meter()")

    def _check_synth_file_extension(self, string: str) -> bool:
        return string.endswith(".scd") or string.endswith(".sc")

    def startup_file_path(self) -> str | None:
        return self._startup_file

    def load_custom_synthdefs(self) -> None:
        buffer = ""
        loaded_synthdefs_message = ["Loaded SynthDefs:"]
        _, _, files = next(walk(self._synth_directory))

        # Filter by file extension (only .sc and .scd)
        files = [f for f in files if self._check_synth_file_extension(f)]
        if len(files) > 0:
            for fname in files:
                with open(self._synth_directory / fname) as infile:
                    for line in infile:
                        buffer += line

            # sending the string to the interpreter
            self._write_stdin(buffer)
            for f in files:
                loaded_synthdefs_message.append("- {}".format(f))
        if len(loaded_synthdefs_message) == 1:
            return
        else:
            print("\n".join(loaded_synthdefs_message))

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
            raise OSError("This OS is not officially supported by Sardine.")

    def boot(self) -> None:
        """Booting a background instance of SCLang!"""
        console = Console()

        with console.status(
            "[yellow][red]Sardine[/red] is booting \
SCLang && SuperDirt...[/yellow]"
        ) as status:
            self._sclang = subprocess.Popen(
                [self._sclang_path],
                stdin=subprocess.PIPE,
                stdout=self.temp_file,
                stderr=self.temp_file,
                bufsize=1,
                universal_newlines=True,
                start_new_session=True,
            )
            if self._startup_file is not None:
                startup_file_path = (
                    str(self._startup_file).replace("\\", "\\\\")
                    if platform.system() == "Windows"
                    else self._startup_file
                )
                self._write_stdin(message="""load("{}")""".format(startup_file_path))

    def kill(self) -> None:
        """Kill the connexion with the SC Interpreter"""
        self._write_stdin("Server.killAll")
        self._write_stdin("0.exit")
