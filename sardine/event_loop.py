import asyncio
import sys
import time

from rich import print

__all__ = ("inject_policy",)


class PerfCounterMixin:
    def time(self) -> float:
        return time.perf_counter()


if hasattr(asyncio, "ProactorEventLoop"):
    class PrecisionProactorEventLoop(PerfCounterMixin, asyncio.ProactorEventLoop):
        ...
else:
    PrecisionProactorEventLoop = None


class PrecisionEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    _loop_factory = PrecisionProactorEventLoop


def _inject_uvloop() -> bool:
    try:
        import uvloop
    except ImportError:
        print("[green]uvloop[/green] [yellow]is not installed")
        return False

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    print("[yellow]Injected uvloop event loop")
    return True


def _inject_precision() -> bool:
    if sys.platform != "win32":
        print("[yellow]Skipping precision event loop on non-Windows system")
        return False

    asyncio.set_event_loop_policy(PrecisionEventLoopPolicy())
    print("[yellow]Injected precision event loop")
    return True


def inject_policy():
    methods = (_inject_uvloop, _inject_precision)
    successful = False
    for func in methods:
        successful = func()
        if successful:
            break

    if not successful:
        print("[yellow]Rhythm accuracy may be impacted")
