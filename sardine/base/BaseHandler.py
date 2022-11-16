from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Hashable, Optional

if TYPE_CHECKING:
    from ..FishBowl import FishBowl


class BaseHandler(ABC, Hashable):
    """Handles particular events that are dispatched by a fish bowl.

    To add a handler to a fish bowl, the `FishBowl.add_handler()` method
    should be called.

    Unlike the fish bowl's concept of "hooks", handlers can apply themselves
    to multiple events at once and have access to the fish bowl via
    the `env` attribute.

    Handlers can only be tied to one fish bowl at a time.
    """

    def __init__(self):
        self.env: "Optional[FishBowl]" = None

    def __call__(self, *args, **kwargs):
        """Calls the handler's `hook()` method."""
        self.hook(*args, **kwargs)

    def setup(self):
        """Called when the handler is added to a fish bowl.

        This method can be used to register itself on specific
        (or all) events with `FishBowl.register_hook(event, self)`.

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
