# https://github.com/python/cpython/blob/main/Lib/asyncio/__main__.py
# Taken from the CPython Github Repository. Custom version of the
# asyncio REPL that will autoload Sardine whenever started.

import concurrent.futures
import threading
import platform
import warnings
import inspect
import asyncio
import psutil
import types
import code
import ast
import os

from appdirs import user_data_dir
from asyncio import futures
from pathlib import Path
from rich import print as pretty_print
from rich.panel import Panel

system = platform.system()

# Setting very high priority for this process (time-critical)
warning_text = "[red bold]Run Sardine using administrator priviledges to get \
better_performances[/red bold]"
if system == "Windows":
    try:
        p = psutil.Process(os.getpid())
        p.nice(psutil.HIGH_PRIORITY_CLASS)
    except psutil.AccessDenied:
        pretty_print(Panel.fit(warning_text))
        pass
else:
    try:
        p = psutil.Process(os.getpid())
        p.nice(-20)
    except psutil.AccessDenied:
        pretty_print(Panel.fit(warning_text))
        pass


# Appdirs boilerplate
APP_NAME, APP_AUTHOR = "Sardine", "Bubobubobubo"
USER_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))


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
