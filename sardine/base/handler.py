from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

__all__ = ("BaseHandler",)


class BaseHandler(ABC):
    """Handles particular events that are dispatched by a fish bowl.

    To add a handler to a fish bowl, the `FishBowl.add_handler()` method
    should be called.

    Unlike the fish bowl's concept of "hooks", handlers can apply themselves
    to multiple events at once and have access to the fish bowl via
    the `env` property.

    Handlers can only be tied to one fish bowl at a time.
    """

    def __init__(self):
        self._env: "Optional[FishBowl]" = None

    def __call__(self, *args, **kwargs):
        """Calls the handler's `hook()` method."""
        self.hook(*args, **kwargs)

    @property
    def env(self) -> "Optional[FishBowl]":
        """The fish bowl (a.k.a. environment) that this handler is added to."""
        return self._env

    # Abstract methods

    def setup(self):
        """Called when the handler is added to a fish bowl.

        This method can be used to register itself on specific
        (or all) events with `self.register(event)`.

        The fish bowl will assign itself to the handler's `env` attribute
        beforehand.

        It is also possible to register other handlers/hooks here as well,
        but the fish bowl will not automatically remove those handlers.
        The `teardown()` method should be used to remove those handlers
        afterwards.
        """

    def teardown(self):
        """Called when the handler is being removed from the fish bowl.

        By default, this method does nothing.

        After teardown finishes, the fish bowl will remove any hooks
        and set the `env` attribute to None.
        """

    @abstractmethod
    def hook(self, event: str, *args):
        """Dispatched by the fish bowl for the handler's registered events."""

    # Public methods

    def register(self, event: Optional[str]):
        """Registers the handler for the given event.

        This is a shorthand for doing `self.env.register_hook(event, self)`.
        """
        if self.env is None:
            raise ValueError(
                "handler cannot register hooks until it is added to a FishBowl"
            )

        self.env.register_hook(event, self)

    def unregister(self, event: Optional[str]):
        """Unregisters the handler for the given event.

        This is a shorthand for doing `self.env.unregister_hook(event, self)`.
        """
        if self.env is None:
            raise ValueError(
                "handler cannot unregister hooks until it is added to a FishBowl"
            )

        self.env.unregister_hook(event, self)
