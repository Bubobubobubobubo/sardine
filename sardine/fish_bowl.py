import collections
from typing import TYPE_CHECKING, Hashable, Protocol

from .sequences.LexerParser.ListParser import ListParser
from .sequences.Iterators import Iterator
from .sequences.Variables import Variables
from .clock.InternalClock import Clock
from .clock.LinkClock import LinkClock

if TYPE_CHECKING:
    from .base.handler import BaseHandler
    from .clock.Time import Time
    from .base.clock import BaseClock
    from .base.parser import BaseParser


class HookProtocol(Hashable, Protocol):
    """A callable object that accepts an event and any number of arguments."""
    def __call__(self, event: str, *args): ...


class FishBowl:
    """Contains all the components necessary to run the Sardine system."""
    def __init__(
        self,
        time: "Time",
    ):
        self.time = time
        # self.clock = Clock(env=self, tempo=120, bpb=4)
        self.clock = LinkClock(env=self, tempo=120, bpb=4)
        self.iterators = Iterator()
        self.variables = Variables()
        self.handlers: "set[BaseHandler]" = set()
        self.parser = ListParser(env=self)

        self.event_hooks: dict[str, set[HookProtocol]] = collections.defaultdict(set)
        # Reverse mapping for easier removal of hooks
        self.hook_events: dict[HookProtocol, set[str]] = collections.defaultdict(set)

    # Hot-swap methods (may be removed in favour of manual replacement)

    def swap_clock(self, clock: "BaseClock", **kwargs):
        """Hot-swap current clock for a different clock.

        Args:
            clock (BaseClock): Target clock
            **kwargs: argument for the new clock
        """
        self.clock.stop()
        self.clock = Clock(
            env=self,
            tempo=self.clock.tempo,
            bpb= self.clock._beats_per_bar)
        self.clock.start()

    def swap_parser(self, parser: "BaseParser"):
        """Hot-swap current parser for a different parser.

        Args:
            parser (BaseParser): New Parser
        """
        self.parser = parser(env=self)

    # Handler management

    def add_handler(self, handler: "BaseHandler"):
        """Adds a new handler to the fish bowl.

        This handler will receive all messages currently dispatched
        in the environment and react accordingly.

        This method is idempotent; adding the handler more than once
        will cause nothing to happen. However, handler objects cannot be
        shared across different fish bowls.

        Args:
            handler (BaseHandler): Sender

        Raises:
            ValueError:
                The handler has already been added to a different fish bowl.
        """
        if handler.env is not None:
            if handler.env is self:
                return
            raise ValueError(f'{handler!r} is already being used by {handler.env!r}')

        handler.env = self
        handler.setup()
        self.handlers.add(handler)

    def remove_handler(self, handler: "BaseHandler"):
        """Removes an existing handler from the fish bowl.

        After a handler has been removed, it can be re-used in new fish bowls.

        This method is idempotent; removing the handler when
        it has already been removed will cause nothing to happen.

        Args:
            handler (BaseHandler): The handler to remove from the fish bowl.
        """
        if handler not in self.handlers:
            return

        handler.teardown()
        handler.env = None

        event_set = self.hook_events.get(handler)
        if event_set is None:
            return

        for event in event_set:
            self.unregister_hook(event, handler)

    # Hook management

    def register_hook(self, event: str, hook: HookProtocol):
        """Registers a hook for a given event.

        This method is idempotent; registering the same hook for
        the same event will cause nothing to happen.

        Args:
            event (str): The event name under which the hook will be registered.
            hook (HookProtocol):
                The hook to call whenever the event is triggered.
        """
        hook_set = self.event_hooks.get(event)
        if hook_set is None or hook in hook_set:
            return

        hook_set.add(hook)
        self.hook_events[hook].add(event)

    def unregister_hook(self, event: str, hook: HookProtocol):
        """Unregisters a hook for a specific event.

        This method is idempotent; unregistering a hook that does not
        exist for a given event will cause nothing to happen.

        Args:
            event (str): The event to remove the hook from.
            hook (HookProtocol): The hook being removed.
        """
        hook_set = self.event_hooks.get(event)
        if hook_set is None or hook not in hook_set:
            return

        hook_set.discard(hook)
        if not hook_set:
            del self.event_hooks[event]

        event_set = self.hook_events.get(hook)
        if event_set is None:
            return

        event_set.discard(event)
        if not event_set:
            del self.hook_events[hook]

    def dispatch(self, event: str, *args):
        """Dispatches an event to it associated hooks with the given arguments.

        Args:
            event (str): The name of the event being dispatched.
            *args: The arguments to pass to the event.
        """
        hook_set = self.event_hooks.get(event)
        if hook_set is None:
            return

        for hook in hook_set:
            hook(event, *args)
