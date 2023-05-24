from typing import Awaitable, Callable, TypeVar, Union

__all__ = ("MaybeCoroFunc", "T")

T = TypeVar("T")
MaybeCoroFunc = Callable[..., Union[T, Awaitable[T]]]
