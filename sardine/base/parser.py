from abc import ABC, abstractmethod
from typing import Any

from .handler import BaseHandler

__all__ = ("BaseParser",)


class BaseParser(BaseHandler, ABC):
    """The interface that fish bowl parsers are expected to implement."""

    @abstractmethod
    def parse(self, expr: str) -> Any:
        """Parses the given string into a value."""
