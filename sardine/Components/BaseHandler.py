from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..clock.FishBowl import Environment

class BaseHandler(ABC):
    @abstractmethod
    def setup(self, env: "Environment"):
        """Called when the handler is added to an environment."""
        # self.env = env perhaps

    @abstractmethod
    def hook(self, event: str, *args, **kwargs):
        """This is called on every event dispatched by the environment."""
        # event might also be an enum, but it simply denotes what event
        # occurred and the handler can filter for events its interested in 
