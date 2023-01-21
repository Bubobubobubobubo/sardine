# https://github.com/python/cpython/blob/main/Lib/asyncio/__main__.py
# Taken from the CPython Github Repository. Custom version of the
# asyncio REPL that will autoload Sardine whenever started.

import ast
import asyncio
import code
import concurrent.futures
import inspect

# import os
# import platform
import threading
import types
import warnings
from asyncio import futures
from pathlib import Path
from typing import Optional

# import psutil
from appdirs import user_data_dir
from rich import print as pretty_print
from rich.panel import Panel

import sardine

from .runners import Runner

# system = platform.system()
# # Setting very high priority for this process (time-critical)
# warning_text = "[yellow]/!\\\\[/yellow] [red bold]  Run Sardine faster by starting it using\
# \nadministrator priviledges (sudo on Unix..)[/red bold] [yellow]/!\\\\[/yellow]"
# if system == "Windows":
#     try:
#         p = psutil.Process(os.getpid())
#         p.nice(psutil.HIGH_PRIORITY_CLASS)
#     except psutil.AccessDenied:
#         pretty_print(Panel.fit(warning_text))
#         pass
# else:
#     try:
#         p = psutil.Process(os.getpid())
#         p.nice(-20)
#     except psutil.AccessDenied:
#         pretty_print(Panel.fit(warning_text))
#         pass


# Appdirs boilerplate
APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))


class AsyncIOInteractiveConsole(code.InteractiveConsole):
    def __init__(self, locals: dict, loop: asyncio.BaseEventLoop):
        super().__init__(locals)
        self.compile.compiler.flags |= ast.PyCF_ALLOW_TOP_LEVEL_AWAIT

        self.loop = loop
        self.repl_future: Optional[asyncio.Task] = None
        self.repl_future_interrupted = False

    def _callback(self, future: concurrent.futures.Future, code: types.CodeType):
        self.repl_future = None
        self.repl_future_interrupted = False

        func = types.FunctionType(code, self.locals)
        try:
            coro = func()
        except SystemExit:
            raise
        except KeyboardInterrupt as ex:
            self.repl_future_interrupted = True
            future.set_exception(ex)
            return
        except BaseException as ex:
            future.set_exception(ex)
            return

        if not inspect.iscoroutine(coro):
            future.set_result(coro)
            return

        try:
            self.repl_future = self.loop.create_task(coro)
            futures._chain_future(self.repl_future, future)
        except BaseException as exc:
            future.set_exception(exc)

    def runcode(self, code: types.CodeType):
        future = concurrent.futures.Future()

        self.loop.call_soon_threadsafe(self._callback, future, code)

        try:
            return future.result()
        except SystemExit:
            raise
        except BaseException:
            if self.repl_future_interrupted:
                self.write("\nKeyboardInterrupt\n")
            else:
                self.showtraceback()


class REPLThread(threading.Thread):
    def __init__(self, *args, console: AsyncIOInteractiveConsole, **kwargs):
        super().__init__(*args, **kwargs)
        self.console = console

    def run(self):
        try:
            banner = ()
            self.console.push("""import os""")
            self.console.push("""os.environ['SARDINE_INIT_SESSION'] = 'YES'""")
            self.console.push("""from sardine.run import *""")
            self.console.interact(banner=banner, exitmsg="exiting asyncio REPL...")
        finally:
            warnings.filterwarnings(
                "ignore",
                message=r"^coroutine .* was never awaited$",
                category=RuntimeWarning,
            )


async def run_forever():
    loop = asyncio.get_running_loop()
    await loop.create_future()


class ConsoleManager:

    def __init__(self):
        self.loop = sardine.event_loop.new_event_loop()

        repl_locals = {"asyncio": asyncio}
        for key in (
            "__name__",
            "__package__",
            "__loader__",
            "__spec__",
            "__builtins__",
            "__file__",
        ):
            repl_locals[key] = globals()[key]

        self.console = AsyncIOInteractiveConsole(repl_locals, self.loop)


    def start(self):
        try:
            import readline  # NoQA
        except ImportError:
            pass

        repl_thread = REPLThread(console=self.console)
        repl_thread.daemon = True
        repl_thread.start()

        with Runner(loop=self.loop) as runner:
            while True:
                try:
                    runner.run(run_forever())
                except KeyboardInterrupt:
                    if self.console.repl_future and not self.console.repl_future.done():
                        self.console.repl_future.cancel()
                        self.console.repl_future_interrupted = True
                    else:
                        break
                else:
                    break
