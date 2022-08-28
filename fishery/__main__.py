import ast
import asyncio
import code
import concurrent.futures
import json
import inspect
import sys
from appdirs import user_data_dir
import threading
import types
import warnings
from asyncio import futures
from pathlib import Path
from dataclasses import dataclass
from typing import Union

APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))


@dataclass
class Config:
    midi: Union[str, None]
    beats: int
    parameters: list
    ppqn: int
    bpm: int
    inline_editor: bool
    superdirt_config_path: str
    verbose_superdirt: bool
    user_config_path: str
    boot_superdirt: bool
    active_clock: bool
    deferred_scheduling: bool

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        config = data["config"]
        return cls(
            midi=config["midi"],
            beats=config["beats"],
            parameters=config["parameters"],
            ppqn=config["ppqn"],
            bpm=config["bpm"],
            inline_editor=config["inline_editor"],
            boot_superdirt=config["boot_superdirt"],
            verbose_superdirt=config["verbose_superdirt"],
            active_clock=config["active_clock"],
            superdirt_config_path=config["superdirt_config_path"],
            user_config_path=config["user_config_path"],
            deferred_scheduling=config["deferred_scheduling"],
        )

    def to_dict(self) -> dict:
        return {
            "config": {
                "midi": self.midi,
                "beats": self.beats,
                "parameters": self.parameters,
                "ppqn": self.ppqn,
                "bpm": self.bpm,
                "inline_editor": self.inline_editor,
                "boot_superdirt": self.boot_superdirt,
                "verbose_superdirt": self.verbose_superdirt,
                "superdirt_config_path": self.superdirt_config_path,
                "active_clock": self.active_clock,
                "user_config_path": self.user_config_path,
                "deferred_scheduling": self.deferred_scheduling,
            }
        }


def read_configuration_file(file_path: Path) -> Config:
    """Read config JSON File"""
    with open(file_path, "r") as f:
        user_data = json.load(f)
    config = Config.from_dict(user_data)
    return config


config = read_configuration_file(USER_DIR / "config.json")
INLINE = config.inline_editor


class AsyncIOInteractiveConsole(code.InteractiveConsole):
    def __init__(self, locals, loop):
        super().__init__(locals)
        self.compile.compiler.flags |= ast.PyCF_ALLOW_TOP_LEVEL_AWAIT

        self.loop = loop

    def runcode(self, code):
        future = concurrent.futures.Future()

        def callback():
            global repl_future
            global repl_future_interrupted

            repl_future = None
            repl_future_interrupted = False

            func = types.FunctionType(code, self.locals)
            try:
                coro = func()
            except SystemExit:
                raise
            except KeyboardInterrupt as ex:
                repl_future_interrupted = True
                future.set_exception(ex)
                return
            except BaseException as ex:
                future.set_exception(ex)
                return

            if not inspect.iscoroutine(coro):
                future.set_result(coro)
                return

            try:
                repl_future = self.loop.create_task(coro)
                futures._chain_future(repl_future, future)
            except BaseException as exc:
                future.set_exception(exc)

        loop.call_soon_threadsafe(callback)

        try:
            return future.result()
        except SystemExit:
            raise
        except BaseException:
            if repl_future_interrupted:
                self.write("\nKeyboardInterrupt\n")
            else:
                self.showtraceback()


class REPLThread(threading.Thread):
    def run(self):
        try:
            banner = ()
            console.push("""from sardine import *""")
            if INLINE:
                console.push("""from ptpython.repl import embed""")
                console.push(
                    """await embed(locals=locals(), globals=globals(), return_asyncio_coroutine=True,patch_stdout=True)"""
                )
            console.interact(banner=banner, exitmsg="exiting asyncio REPL...")

        finally:
            warnings.filterwarnings(
                "ignore",
                message=r"^coroutine .* was never awaited$",
                category=RuntimeWarning,
            )

            loop.call_soon_threadsafe(loop.stop)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    repl_locals = {"asyncio": asyncio}
    for key in {
        "__name__",
        "__package__",
        "__loader__",
        "__spec__",
        "__builtins__",
        "__file__",
    }:
        repl_locals[key] = locals()[key]

    console = AsyncIOInteractiveConsole(repl_locals, loop)

    repl_future = None
    repl_future_interrupted = False

    try:
        import readline  # NoQA
    except ImportError:
        pass

    repl_thread = REPLThread()
    repl_thread.daemon = True
    repl_thread.start()

    while True:
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            if repl_future and not repl_future.done():
                repl_future.cancel()
                repl_future_interrupted = True
            continue
        else:
            break
