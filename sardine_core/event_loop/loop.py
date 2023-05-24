import asyncio

from .mixin import PerfCounterMixin
from .sansio import SansIOEventLoop

__all__ = (
    "PrecisionProactorEventLoop",
    "PrecisionSansIOEventLoop",
    "PrecisionSelectorEventLoop",
)


if hasattr(asyncio, "ProactorEventLoop"):

    class PrecisionProactorEventLoop(PerfCounterMixin, asyncio.ProactorEventLoop):
        ...

else:
    PrecisionProactorEventLoop = None


class PrecisionSansIOEventLoop(PerfCounterMixin, SansIOEventLoop):
    ...


class PrecisionSelectorEventLoop(PerfCounterMixin, asyncio.SelectorEventLoop):
    ...
