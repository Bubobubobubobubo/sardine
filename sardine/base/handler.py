from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..fish_bowl import FishBowl

__all__ = ("BaseHandler",)


class BaseHandler:
    """Handles particular events that are dispatched by a fish bowl.

    To add a handler to a fish bowl, the `FishBowl.add_handler()` method
    should be called. Handlers can only be tied to one fish bowl at a time.

    Unlike the fish bowl's concept of "hooks", handlers can apply themselves
    to multiple events at once and have access to the fish bowl via
    the `env` property.

    Handlers can also be given "child handlers" using the
    `BaseHandler.add_child()` method. Whenever a parent handler is added
    to a fish bowl, its children are automatically added afterwards.
    Likewise, when a parent handler is removed, its children are also removed.

    Child handlers can still be manually removed from the fish bowl
    after being added. However, child handlers cannot be added to a
    fish bowl before the parent handler is added, or be added to
    a fish bowl different than the parent's handler.

    This class can also be used directly for grouping handlers that don't
    necessarily require anything from each other::

        group = BaseHandler(lock_children=True)
        group.add_child(SomeHandler())
        group.add_child(AnotherHandler())

    However, if those handlers do depend on each other, it is recommended
    to subclass this and add them as attributes of the group, making the
    handlers available through the `parent` attribute.

    Args:
        lock_children (Optional[bool]):
            If True, any child handlers are required to share the same
            fish bowl as the parent. Once its children are added to
            a fish bowl, they cannot be removed by themselves, and the
            parent must be removed instead.
            If False, child handlers are freely removable.
            If None, this will be deferred to the parent handler's setting.
            For handlers without a parent, None is equivalent to False.
    """

    def __init__(self, *, lock_children: Optional[bool] = None):
        self.lock_children = lock_children
        self._env: "Optional[FishBowl]" = None
        self._children: list[BaseHandler] = []
        self._parent: Optional[BaseHandler] = None

    def __call__(self, *args, **kwargs):
        """Calls the handler's `hook()` method."""
        self.hook(*args, **kwargs)

    def __repr__(self) -> str:
        return "<{} {}>".format(
            type(self).__name__,
            " ".join(
                f"{attr}={getattr(self, attr)}"
                for attr in (
                    "lock_children",
                    "env",
                )
            ),
        )

    @property
    def children(self) -> "list[BaseHandler]":
        """A list of this handler's immediate children."""
        return self._children.copy()

    @property
    def env(self) -> "Optional[FishBowl]":
        """The fish bowl (a.k.a. environment) that this handler is added to."""
        return self._env

    @property
    def locked(self) -> bool:
        """Indicates if this handler is locked by one of its parent handlers."""
        if self.parent is None:
            return False
        elif self.parent.lock_children is None:
            return self.parent.locked
        return self.parent.lock_children

    @property
    def parent(self) -> "Optional[BaseHandler]":
        """The parent of this handler, if any."""
        return self._parent

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

    def hook(self, event: str, *args):
        """Dispatched by the fish bowl for the handler's registered events."""

    # Public methods

    def add_child(self, handler: "BaseHandler"):
        """Adds another handler as a child of this handler.

        If the parent handler is already added to a fish bowl, this
        method will *not* add the child handler to the same fish bowl.
        The child handler can still be added to the parent's fish bowl
        before or after this is called.

        This method is idempotent; adding the handler more than once
        will cause nothing to happen. However, child handlers cannot
        be shared with other parent handlers.

        WARNING: this method does not prevent cyclic references from
        occurring. Behaviour is undefined when a handler adds any of
        its ancestors as a child of itself.

        Args:
            handler (BaseHandler): The handler being added.

        Raises:
            ValueError:
                The handler is either already added to a fish bowl other than
                the parent, or is already a child of a different handler,
                or was attempting to add itself as a child.

        """
        if handler is self:
            raise ValueError(f"{handler!r} cannot be a child of itself")
        elif handler.env is not None and handler.env is not self.env:
            raise ValueError(f"{handler!r} is already being used by {handler.env!r}")
        elif handler.parent is not None:
            # FIXME: proper handler cyclic reference prevention (ancestors/descendents)
            if handler.parent is self:
                return
            raise ValueError(f"{handler!r} is already a child of {handler.parent!r}")

        handler._parent = self  # pylint: disable=protected-access
        self._children.append(handler)

    def remove_child(self, handler: "BaseHandler"):
        """Removes an existing child handler from this handler.

        If the child handler was already set up, this method will *not*
        remove the child handler from the fish bowl.

        After a handler has been removed, it can be re-used in new fish bowls.

        This method is idempotent; removing the handler when
        it has already been removed will cause nothing to happen.

        Args:
            handler (BaseHandler): The child handler to remove.
        """
        try:
            i = self._children.index(handler)
        except ValueError:
            return

        # The statement below is intentionally commented to let locked
        # handlers unbind themselves from their parent if desired:
        # if handler.env is not None and handler.locked:
        #     raise ValueError(f"{handler!r} has been locked by its parent")

        handler._parent = None  # pylint: disable=protected-access
        self._children.pop(i)

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
