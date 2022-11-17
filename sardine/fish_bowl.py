import collections
from asyncio import Event
from typing import (
    TYPE_CHECKING,
    Hashable,
    Iterable,
    Optional,
    Protocol,
    Union)

from exceptiongroup import BaseExceptionGroup

from .sequences.SardineParser.ListParser import ListParser
from .sequences.Iterators import Iterator
from .sequences.Variables import Variables
from .clock.InternalClock import Clock
from .clock.LinkClock import LinkClock
from .clock.Time import Time
from .handlers.SleepHandler import SleepHandler

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
    def __init__(self):
        self.time = Time(self)
        self._alive = Event()
        self._resumed = Event()
        self.iterators = Iterator()
        self.variables = Variables()
        self.handlers: "set[BaseHandler]" = set()
        self.parser = None

        self.event_hooks: dict[Optional[str], set[HookProtocol]] = collections.defaultdict(set)
        # Reverse mapping for easier removal of hooks
        self.hook_events: dict[HookProtocol, set[Optional[str]]] = collections.defaultdict(set)

        # Add the base SleepHandler
        self.handlers.add(SleepHandler(env=self))

        # Send a start() signal so that time can start now


    ## TRANSPORT ######################################################################

    def pause(self):
        if self._resumed.is_set():
            self._resumed.clear()
        self.dispatch("pause")

    def resume(self):
        if not self._resumed.is_set():
            self._resumed.set()
        self.dispatch("resume")

    def start(self):
        if not self._alive.is_set():
            self._alive.set()
        self.dispatch("start")

    def stop(self):
        if self._alive.set():
            self._alive.clear()
        self.dispatch("stop")

    def is_paused(self):
        return not self._resumed.is_set()

    def is_running(self):
        return self._alive.is_set()

    ## SLEEPING MANAGEMENT ############################################################

    async def sleep(self, duration: Union[int, float]):
        """Sleep method for the SleepHandler"""
        # ???

    # Hot-swap methods ############################################################

    def swap_parser(self, parser: "BaseParser"):
        """Hot-swap current parser for a different parser.

        Args:
            parser (BaseParser): New Parser
        """
        self.parser = parser(env=self)

    def swap_clock(self, clock: 'BaseClock'):
        """Hot-swap current clock for a different clock"""
        # 1) pause the fish bowl
        # 2) remove the old clock's handler
        # 3) replace with the current clock and add as handler
        # 4) resume fish bowl
        # 5) Trigger a clock_swap event with one argument, the new BaseClock object
        pass

    ## HANDLERS ############################################################

    def add_handler(self, handler: "BaseHandler"):
        """Adds a new handler to the fish bowl.

        This handler will receive all messages currently dispatched
        in the environment and react accordingly.

        This method is idempotent; adding the handler more than once
        will cause nothing to happen. However, handler objects cannot
        be shared across different fish bowls.

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

        # It may be possible that the user set `env` to None, but
        # given that `register_hook()` is idempotent, it's probably
        # fine to call `BaseHandler.setup()` again

        handler._env = self  # pylint: disable=protected-access
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
        handler._env = None  # pylint: disable=protected-access
        self.handlers.remove(handler)

        event_set = self.hook_events.get(handler)
        if event_set is not None:
            for event in event_set:
                self.unregister_hook(event, handler)

    # Hook management

    def register_hook(self, event: Optional[str], hook: HookProtocol):
        """Registers a hook for a given event.

        Whenever the fish bowl dispatches an event, the hooks associated
        with that event will be called in an arbitrary order.

        Global hooks can also be registered by passing `None` as the event.
        These hooks will be called on every event that is dispatched.
        If a hook is registered both globally and for a specific event,
        the hook will always be called once regardless.

        This method is idempotent; registering the same hook for
        the same event will cause nothing to happen.

        Args:
            event (Optional[str]):
                The event name under which the hook will be registered.
                If set to `None`, this will be a global hook.
            hook (HookProtocol):
                The hook to call whenever the event is triggered.
        """
        hook_set = self.event_hooks[event]
        if hook in hook_set:
            return

        hook_set.add(hook)
        self.hook_events[hook].add(event)

    def unregister_hook(self, event: Optional[str], hook: HookProtocol):
        """Unregisters a hook for a specific event.

        Global hooks can be removed by passing `None` as the event.

        This method is idempotent; unregistering a hook that does not
        exist for a given event will cause nothing to happen.

        Args:
            event (Optional[str]): The event to remove the hook from.
            hook (HookProtocol): The hook being removed.
        """
        hook_set = self.event_hooks.get(event)
        if hook_set is not None:
            hook_set.discard(hook)
            if not hook_set:
                del self.event_hooks[event]

        event_set = self.hook_events.get(hook)
        if event_set is not None:
            event_set.discard(event)
            if not event_set:
                del self.hook_events[hook]

    def _run_hooks(self, hooks: Iterable[HookProtocol], event: str, *args):
        exceptions: list[BaseException] = []
        for func in hooks:
            try:
                func(event, *args)
            # pylint: disable=invalid-name,broad-except
            except Exception as e:
                exceptions.append(e)
            except BaseException as e:
                exceptions.append(e)
                break
            # pylint: enable=invalid-name,broad-except

        if exceptions:
            raise BaseExceptionGroup(
                f'Errors raised while running hooks for {event}',
                exceptions
            )


    def dispatch(self, event: str, *args):
        """Dispatches an event to it associated hooks with the given arguments.

        Args:
            event (str): The name of the event being dispatched.
            *args: The arguments to pass to the event.
        """
        empty_set: set[HookProtocol] = set()
        local_hooks = self.event_hooks.get(event, empty_set)
        global_hooks = self.event_hooks.get(None, empty_set)

        all_hooks = local_hooks | global_hooks
        self._run_hooks(all_hooks, event, *args)
