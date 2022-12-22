import importlib
import sys
from pathlib import Path
from string import ascii_lowercase, ascii_uppercase
from typing import Any, Callable, Optional, ParamSpec, TypeVar, Union, overload
from rich import print
from . import *
from .io.UserConfig import read_user_configuration
from .superdirt import SuperDirtProcess
from .utils import config_line_printer, get_snap_deadline, sardine_intro
from .sequences import ZiffersParser, ListParser
from .sequences.sequence import E, mod, imod, pick

P = ParamSpec("P")  # NOTE: name is similar to surfboards
T = TypeVar("T")

#######################################################################################
# READING USER CONFIGURATION (TAKEN FROM SARDINE-CONFIG)

config = read_user_configuration()

# Printing banner and some infos about setup/config
print(sardine_intro)
print(config_line_printer(config))


#######################################################################################
# LOADING USER CONFIGURATION

if Path(f"{config.user_config_path}").is_file():
    spec = importlib.util.spec_from_file_location(
        "user_configuration", config.user_config_path
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    from user_configuration import *
else:
    print(f"[red]No user provided configuration file found...")

# Initialisation of the FishBowl (the environment holding everything together)

clock = LinkClock if config.link_clock else InternalClock
parser = ZiffersParser if config.parser == "ziffers" else ListParser
bowl = FishBowl(
    clock=clock(tempo=config.bpm, bpb=config.beats),
    parser=parser(),
)

#######################################################################################
# OPENING SUPERCOLLIDER/SUPERDIRT SUBPROCESS. DISSOCIATED FROM THE SUPERDIRT HANDLERS.

config = read_user_configuration()
if config.boot_supercollider:
    try:
        SC = SuperDirtProcess(
            startup_file=(
                config.superdirt_config_path if config.sardine_boot_file else None
            ),
            verbose=config.verbose_superdirt,
        )
    except OSError as Error:
        print(f"[red]SuperCollider could not be found: {Error}![/red]")

#######################################################################################
# HANDLERS INITIALIZATION. YOU CAN ADD YOUR MODULAR COMPONENTS HERE.

# MIDI Handler: matching with the MIDI port defined in the configuration file
midi = MidiHandler(port_name=str(config.midi))
bowl.add_handler(midi)

# OSC Loop: handles processing OSC messages
osc_loop = OSCLoop()
bowl.add_handler(osc_loop)  # NOTE: always keep this loop running for OSC handlers

# OSC Handler: dummy OSC handler, mostly used for test purposes
dummy_osc = OSCHandler(
    ip="127.0.0.1",
    port=12345,
    name="Custom OSC Connexion",
    ahead_amount=0.0,
    loop=osc_loop,
)
O = dummy_osc.send

# # OSC Listener Handler: dummy OSCIn handler, used for test purposes
# my_osc_listener = OSCInHandler(
#     ip="127.0.0.1", port=33333, name="OSC-In test", loop=my_osc_loop
# )

# SuperDirt Handler: conditional
if config.superdirt_handler:
    dirt = SuperDirtHandler(loop=osc_loop)

# Adding Players
player_names = ["P" + l for l in ascii_lowercase + ascii_uppercase]
for player in player_names:
    p = Player(name=player)
    globals()[player] = p
    bowl.add_handler(p)


#######################################################################################
# BASIC MECHANISMS: SWIMMING, DELAY, SLEEP AND OTHER IMPORTANT CONSTRUCTS


@overload
def swim(
    func: Union[Callable[P, T], AsyncRunner],
    /,
    # NOTE: AsyncRunner doesn't support generic args/kwargs
    *args: P.args,
    snap: Optional[Union[float, int]] = 0,
    **kwargs: P.kwargs,
) -> AsyncRunner:
    ...


@overload
def swim(
    func: None,
    /,
    *args: P.args,
    snap: Optional[Union[float, int]] = 0,
    **kwargs: P.kwargs,
) -> Callable[[Callable[P, T]], AsyncRunner]:
    ...


# pylint: disable=keyword-arg-before-vararg  # signature is valid
def swim(func=None, /, *args, snap=0, **kwargs):
    """
    Swimming decorator: push a function to the scheduler. The function will be
    declared and followed by the scheduler system to recurse in time if needed.

    Args:
        func (Optional[Union[Callable[P, T], AsyncRunner]]):
            The function to be scheduled. If this is an AsyncRunner,
            the current state is simply updated with new arguments.
        *args: Positional arguments to be passed to `func.`
        snap (Optional[Union[float, int]]):
            If set to a numeric value, the new function will be
            deferred until the next bar + `snap` beats arrives.
            If None, the function is immediately pushed and will
            run on its next interval.
            If `func` is an AsyncRunner, this parameter has no effect.
        **kwargs: Keyword arguments to be passed to `func.`
    """

    def decorator(func: Union[Callable, AsyncRunner]) -> AsyncRunner:
        if isinstance(func, AsyncRunner):
            func.update_state(*args, **kwargs)
            bowl.scheduler.start_runner(func)
            return func

        runner = bowl.scheduler.get_runner(func.__name__)
        if runner is None:
            runner = AsyncRunner(func.__name__)

        # Runners normally allow the same functions to appear in the stack,
        # but we will treat repeat functions as just reloading the runner
        if runner.states and runner.states[-1].func is func:
            again(runner)
            bowl.scheduler.start_runner(runner)
            return runner
        elif snap is not None:
            deadline = get_snap_deadline(bowl.clock, snap)
            runner.push_deferred(deadline, func, *args, **kwargs)
        else:
            runner.push(func, *args, **kwargs)

        # Intentionally avoid interval correction so
        # the user doesn't accidentally nudge the runner
        runner.swim()
        runner.reload()

        bowl.scheduler.start_runner(runner)
        return runner

    if func is not None:
        return decorator(func)
    return decorator


def again(runner: AsyncRunner, *args, **kwargs):
    """
    Keep a runner swimming. User functions should continuously call this
    at the end of their function until they want the function to stop.
    """
    runner.update_state(*args, **kwargs)
    runner.swim()
    # If this is manually called we should wake up the runner sooner
    runner.reload()


def die(func: Union[Callable, AsyncRunner]) -> AsyncRunner:
    """
    Swimming decorator: remove a function from the scheduler. The function
    will not be called again and will likely stop recursing in time.
    """
    if isinstance(func, AsyncRunner):
        bowl.scheduler.stop_runner(func)
        return func

    runner = bowl.scheduler.get_runner(func.__name__)
    if runner is not None:
        bowl.scheduler.stop_runner(runner)
    else:
        runner = AsyncRunner(func.__name__)
        runner.push(func)
    return runner


def sleep(n_beats: Union[int, float]):
    """Artificially sleep in the current function for `n_beats`.

    Example usage: ::

        @swim
        def func(p=4):
            sleep(3)
            for _ in range(3):
                S('909').out()
                sleep(1/2)
            again(func)

    This should *only* be called inside swimming functions.
    Unusual behaviour may occur if sleeping is done globally.

    Using in asynchronous functions
    -------------------------------

    This can be used in `async def` functions and does *not* need to be awaited.

    Sounds scheduled in asynchronous functions will be influenced by
    real time passing. For example, if you sleep for 500ms (based on tempo)
    and await a function that takes 100ms to complete, any sounds sent
    afterwards will occur 600ms from when the function was called.

    ::

        @swim
        async def func(p=4):
            print(bowl.clock.time)  # 0.0s

            sleep(1)     # virtual +500ms (assuming bowl.clock.tempo = 120)
            await abc()  # real +100ms

            S('bd').out()           # occurs 500ms from now
            print(bowl.clock.time)  # 0.6s
            again(func)

    Technical Details
    -----------------

    Unlike `time.sleep(n)`, this function does not actually block
    the function from running. Instead, it temporarily affects the
    value of `BaseClock.time` and extends the perceived time of methods
    using that property, like `SleepHandler.wait_after()`
    and `BaseClock.get_beat_time()`.

    In essence, this maintains the precision of sound scheduling
    without requiring the use of declarative syntax like
    `S('909', at=1/2).out()`.

    """
    duration = bowl.clock.get_beat_time(n_beats, sync=False)
    bowl.time.shift += duration


def silence(*runners: AsyncRunner) -> None:
    """
    Silence is capable of stopping one or all currently running swimming functions. The
    function will also trigger a general MIDI note_off event (all channels, all notes).
    This function will only kill events on the Sardine side. For a function capable of
    killing synthesizers running on SuperCollider, try the more potent 'panic' function.
    """
    if len(runners) == 0:
        midi.all_notes_off()
        bowl.scheduler.reset()
        return

    for run in runners:
        bowl.scheduler.stop_runner(run)


def panic(*runners: AsyncRunner) -> None:
    """
    If SuperCollider/SuperDirt is booted, panic acts as a more powerful alternative to
    silence() capable of killing synths on-the-fly. Use as a last ressource if you are
    loosing control of the system.
    """
    silence(*runners)
    if config.superdirt_handler:
        D("superpanic")


def Pat(pattern: str, i: int = 0, div: int = 1, rate: int = 1) -> Any:
    """
    General purpose pattern interface. This function can be used to summon the global
    parser stored in the fish_bowl. It is generally used to pattern outside of the
    handler/sender system, if you are playing with custom libraries, imported code or
    if you want to take the best of the patterning system without having to deal with
    all the built-in I/O.

    Args:
        pattern (str): A pattern to be parsed
        i (int, optional): Index for iterators. Defaults to 0.

    Returns:
        int: The ith element from the resulting pattern
    """
    result = bowl.parser.parse(pattern)
    return Sender.pattern_element(result, i, div, rate)


class Delay:
    """
    Delay is a compound statement providing an alternative syntax to the overridden
    sleep() method. It implements the bare minimum to reproduce sleep behavior using
    extra indentation for marking visually where sleep takes effect.
    """

    def __init__(self, duration: Union[int, float] = 1, delayFirst: bool = True):
        self.duration = duration
        self.delayFirst = delayFirst

    def __call__(self, duration=1, delayFirst=False):
        self.duration = duration
        self.delayFirst = delayFirst
        return self

    def __enter__(self):
        if self.delayFirst:
            sleep(self.duration)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.delayFirst:
            sleep(self.duration)


#######################################################################################
# DEFINITION OF ALIASES

clock = bowl.clock

I, V = bowl.iterators, bowl.variables  # Iterators and Variables from env
P = Pat  # Generic pattern interface
N = midi.send  # For sending MIDI Notes
PC = midi.send_program  # For MIDI Program changes
CC = midi.send_control  # For MIDI Control Change messages
play = Player.play


def n(*args, **kwargs):
    return play(midi, midi.send, *args, **kwargs)


def cc(*args, **kwargs):
    return play(midi, midi.send_control, *args, **kwargs)


def pc(*args, **kwargs):
    return play(midi, midi.send_program, *args, **kwargs)


if config.superdirt_handler:
    D = dirt.send

    def d(*args, **kwargs):
        return play(dirt, dirt.send, *args, **kwargs)


#######################################################################################
# CLOCK START: THE SESSION IS NOW LIVE

bowl.start()
