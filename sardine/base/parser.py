from abc import ABC, abstractmethod

__all__ = ("BaseParser",)


# TODO: document BaseParser and its methods
class BaseParser(ABC):
    @abstractmethod
    def parse(self, expression: str):
        pass
