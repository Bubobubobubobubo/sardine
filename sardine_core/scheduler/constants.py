from typing import Awaitable, Callable, TypeVar

__all__ = ("MaybeCoroFunc", "T")

T = TypeVar("T")
MaybeCoroFunc = Callable[..., T | Awaitable[T]]
