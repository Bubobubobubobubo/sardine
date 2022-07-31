# https://stackoverflow.com/questions/53689193/how-to-handle-exceptions-from-any-task-in-an-event-loop

from .clock.Clock import Clock
from .superdirt.Sound import Sound as S
from .superdirt.AutoBoot import (
        SuperColliderProcess,
        find_startup_file,
        find_synth_directory)
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from functools import wraps
import uvloop
import asyncio
import pathlib

# import warnings
# warnings.filterwarnings("ignore")

def print_pre_alpha_todo() -> None:
    """ Print the TODOlist from pre-alpha version """
    cur_path = pathlib.Path(__file__).parent.resolve()
    with open("".join([str(cur_path), "/todo.md"])) as f:
        console = Console()
        console.print(Markdown(f.read()))


sardine = """

░██████╗░█████╗░██████╗░██████╗░██╗███╗░░██╗███████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║████╗░██║██╔════╝
╚█████╗░███████║██████╔╝██║░░██║██║██╔██╗██║█████╗░░
░╚═══██╗██╔══██║██╔══██╗██║░░██║██║██║╚████║██╔══╝░░
██████╔╝██║░░██║██║░░██║██████╔╝██║██║░╚███║███████╗
╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚══╝╚══════╝

Sardine is a small MIDI/OSC sequencer made for live-
coding. Check the examples/ folder to learn more. :)
"""


# Pretty printing
print(f"[red]{sardine}[/red]")
print_pre_alpha_todo()
print('\n')

uvloop.install()
loop = asyncio.get_running_loop()

def my_exception_handler(_, exception):
    print(f"{type(exception)}")

async def handled(coro):
    try:
        await coro
    except IOError:
        print('no IO today')

def factory(loop, coro):
    task = asyncio.create_task(handled(coro))
    return task

loop = asyncio.get_running_loop()
loop.set_exception_handler(my_exception_handler)
loop.set_task_factory(factory)

c = Clock()
cs = c.schedule
cr = c.remove
td = c._get_tick_duration

loop = c._auto_schedule
try:
    asyncio.create_task(c.send_start(initial=True))
except Exception as e:
    print(e)

# Should start, doesn't start
SC = SuperColliderProcess(
        synth_directory=find_synth_directory(),
        startup_file=find_startup_file())

# async def boot_supercollider():
#     await SC.boot()
# asyncio.create_task(boot_supercollider())

def swim(fn):
    @wraps(fn)
    def decorator(fn):
        try:
            cs(fn())
        except Exception:
            pass
    decorator(fn)
    return fn

def die(fn):
    @wraps(fn)
    def decorator(fn):
        try:
            cr(fn)
        except Exception:
            pass
    return decorator(fn)


@swim
async def bd():
    S('bd').out()
    loop(bd())
