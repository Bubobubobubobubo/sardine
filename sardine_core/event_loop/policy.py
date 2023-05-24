import asyncio

from .loop import *

__all__ = (
    "PrecisionProactorEventLoopPolicy",
    "PrecisionSansIOEventLoopPolicy",
    "PrecisionSelectorEventLoopPolicy",
)


class PrecisionProactorEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    _loop_factory = PrecisionProactorEventLoop


class PrecisionSansIOEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    _loop_factory = PrecisionSansIOEventLoop


class PrecisionSelectorEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    _loop_factory = PrecisionSelectorEventLoop
