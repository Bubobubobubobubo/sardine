import asyncio
import time
import threading
from typing import Optional

import rich

__all__ = ("install_policy",)


class PerfCounterMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._clock_resolution = time.get_clock_info("perf_counter").resolution

    def time(self) -> float:
        return time.perf_counter()


class SansSelector:

    _event_list = []

    def __init__(self, wake_cond: threading.Condition):
        self._wake_cond = wake_cond

    def select(self, timeout: Optional[int]):
        timeout = timeout or 0.0
        with self._wake_cond:
            self._wake_cond.wait(timeout)
        return self._event_list


class SansIOEventLoop(asyncio.BaseEventLoop):
    """An event loop implementation with zero I/O support.

    This removes the potential overhead of waiting on I/O from selectors,
    replacing it with `time.sleep()`. Any native I/O APIs will **not** work
    when using this implementation.
    """
    def __init__(self) -> None:
        super().__init__()
        self._wake_cond = wake_cond = threading.Condition()
        self._selector = SansSelector(wake_cond)

    def _process_events(self, event_list):
        pass

    def _write_to_self(self):
        with self._wake_cond:
            self._wake_cond.notify_all()

# Precision mixins

if hasattr(asyncio, "ProactorEventLoop"):

    class PrecisionProactorEventLoop(PerfCounterMixin, asyncio.ProactorEventLoop):
        ...

else:
    PrecisionProactorEventLoop = None


class PrecisionSansIOEventLoop(PerfCounterMixin, SansIOEventLoop):
    ...


class PrecisionSelectorEventLoop(PerfCounterMixin, asyncio.SelectorEventLoop):
    ...

# Policies

class PrecisionProactorEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    _loop_factory = PrecisionProactorEventLoop


class PrecisionSansIOEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    _loop_factory = PrecisionSansIOEventLoop


class PrecisionSelectorEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    _loop_factory = PrecisionSelectorEventLoop

# installors

def _install_precision_proactor() -> bool:
    if PrecisionProactorEventLoop is None:
        rich.print("[yellow]Skipping precision event loop on non-Windows system")
        return False

    asyncio.set_event_loop_policy(PrecisionProactorEventLoopPolicy())
    rich.print("[yellow]Installed precision proactor event loop")
    return True


def _install_precision_sansio() -> bool:
    asyncio.set_event_loop_policy(PrecisionSansIOEventLoopPolicy())
    rich.print("[yellow]installed precision Sans I/O event loop")
    rich.print("[bold red]WARNING: event loop does not networking/subprocesses")
    return True


def _install_precision_selector() -> bool:
    asyncio.set_event_loop_policy(PrecisionSelectorEventLoopPolicy())
    rich.print("[yellow]Installed precision selector event loop")
    return True


def _install_uvloop() -> bool:
    try:
        import uvloop
    except ImportError:
        rich.print("[green]uvloop[/green] [yellow]is not installed")
        return False

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    rich.print("[yellow]Installed uvloop event loop")
    return True


def install_policy():
    """Installs the best-available event loop policy into asyncio.

    This method must be called before any event loop is created, otherwise
    it will not affect those event loops.
    """
    methods = (
        # _install_precision_sansio,
        _install_uvloop,
        _install_precision_proactor,
        _install_precision_selector,
    )
    successful = False
    for func in methods:
        successful = func()
        if successful:
            break

    if not successful:
        rich.print("[yellow]Rhythm accuracy may be impacted")


def new_event_loop() -> asyncio.BaseEventLoop:
    """Creates the best-available event loop without permanently installing
    a new policy for asyncio.
    """
    last_policy = asyncio.get_event_loop_policy()
    install_policy()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop_policy(last_policy)
    return loop
