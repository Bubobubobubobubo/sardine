import asyncio
import time
from typing import Optional

import rich

__all__ = ("inject_policy",)


class PerfCounterMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._clock_resolution = time.get_clock_info("perf_counter").resolution

    def time(self) -> float:
        return time.perf_counter()


class SansSelector:
    _event_list = []

    def select(self, timeout: Optional[int]):
        timeout = timeout or 0.0
        time.sleep(timeout)
        return self._event_list


class SansIOEventLoop(asyncio.BaseEventLoop):
    """An event loop implementation with zero I/O support.

    This removes the potential overhead of waiting on I/O from selectors,
    replacing it with `time.sleep()`. Any native I/O APIs will **not** work
    when using this implementation.
    """

    _selector = SansSelector()

    def _process_events(self, event_list):
        pass

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

# Injectors

def _inject_precision_proactor() -> bool:
    if PrecisionProactorEventLoop is None:
        rich.print("[yellow]Skipping precision event loop on non-Windows system")
        return False

    asyncio.set_event_loop_policy(PrecisionProactorEventLoopPolicy())
    rich.print("[yellow]Injected precision proactor event loop")
    return True


def _inject_precision_sansio() -> bool:
    asyncio.set_event_loop_policy(PrecisionSansIOEventLoopPolicy())
    rich.print("[yellow]Injected precision Sans I/O event loop")
    rich.print("[bold red]WARNING: event loop does not networking/subprocesses")
    return True


def _inject_precision_selector() -> bool:
    asyncio.set_event_loop_policy(PrecisionSelectorEventLoopPolicy())
    rich.print("[yellow]Injected precision selector event loop")
    return True


def _inject_uvloop() -> bool:
    try:
        import uvloop
    except ImportError:
        rich.print("[green]uvloop[/green] [yellow]is not installed")
        return False

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    rich.print("[yellow]Injected uvloop event loop")
    return True


def inject_policy():
    methods = (
        # _inject_precision_sansio,
        _inject_uvloop,
        _inject_precision_proactor,
        _inject_precision_selector,
    )
    successful = False
    for func in methods:
        successful = func()
        if successful:
            break

    if not successful:
        rich.print("[yellow]Rhythm accuracy may be impacted")
