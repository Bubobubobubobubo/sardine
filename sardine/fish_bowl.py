import asyncio
import collections
from typing import Hashable, Iterable, Optional, Protocol, Union

from exceptiongroup import BaseExceptionGroup

from .base import BaseClock, BaseHandler, BaseParser
from .clock import InternalClock, Time
from .handlers import SleepHandler
from .scheduler import Scheduler
from .sequences import Iterator, ListParser, Variables

__all__ = ("FishBowl",)


class HookProtocol(Hashable, Protocol):
    """A callable object that accepts an event and any number of arguments."""

    def __call__(self, event: str, *args):
        ...


class FishBowl:
    """Contains all the components necessary to run the Sardine system."""

    def __init__(
        self,
        clock: Optional[BaseClock] = None,
        iterator: Optional[Iterator] = None,
        parser: Optional[BaseParser] = None,
        scheduler: Optional[Scheduler] = None,
        sleeper: Optional[SleepHandler] = None,
        time: Optional[Time] = None,
        variables: Optional[Variables] = None,
    ):
        self.clock = clock or InternalClock()
        self.iterators = iterator or Iterator()
        self.parser = parser or ListParser()
        self.scheduler = scheduler or Scheduler()
        self.sleeper = sleeper or SleepHandler()
        self.time = time or Time()
        self.variables = variables or Variables()

        self._handlers: dict[BaseHandler, None] = {}
        self._alive = asyncio.Event()
        self._resumed = asyncio.Event()

        self._event_hooks: dict[
            Optional[str], dict[HookProtocol, None]
        ] = collections.defaultdict(dict)
        # Reverse mapping for easier removal of hooks
        self._hook_events: dict[
            HookProtocol, dict[Optional[str], None]
        ] = collections.defaultdict(dict)

        self.add_handler(self.clock)
        self.add_handler(self.parser)
        self.add_handler(self.scheduler)
        self.add_handler(self.sleeper)
        self.add_handler(self.time)

    @property
    def handlers(self) -> list[BaseHandler]:
        """A list of all handlers added to this fish bowl."""
        return list(self._handlers)

    ## DUNDER #################################################################

    def __del__(self):
        self.stop()
        for handler in self.handlers:
            self.remove_handler(handler)

    def __repr__(self) -> str:
        running = self.is_running()
        paused = self.is_paused()
        status = (
            "playing"
            if running and not paused
            else "paused"
            if running and paused
            else "stopped"
        )

        return "<{} {} clock={!r}>".format(
            type(self).__name__,
            status,
            self.clock,
        )

    ## TRANSPORT ##############################################################

    def pause(self) -> bool:
        """Pauses the fish bowl.

        This will emit a `pause` event unless the fish bowl does
        not need to be paused, e.g. being paused once already or not
        having started.

        Returns:
            bool: True if the fish bowl was paused, False otherwise.
        """
        allowed = self.is_running() and not self.is_paused()
        if allowed:
            self._resumed.clear()
            self.dispatch("pause")
        return allowed

    def resume(self) -> bool:
        """Resumes the fish bowl.

        This will emit a `resume` event unless the fish bowl does
        not need to be resumed, e.g. if the clock is not running
        or has not been paused.

        Returns:
            bool: True if the fish bowl was resumed, False otherwise.
        """
        allowed = self.is_running() and self.is_paused()
        if allowed:
            self._resumed.set()
            self.dispatch("resume")
        return allowed

    def start(self) -> bool:
        """Starts the fish bowl.

        This will emit a `start` event unless the fish bowl does
        not need to be started, e.g. if the fish bowl has already started.

        If the fish bowl is started, paused, stopped, and started again,
        handlers should treat it as if the fish bowl is no longer paused.

        Returns:
            bool: True if the fish bowl was started, False otherwise.
        """
        allowed = not self.is_running()
        if allowed:
            self._alive.set()
            self._resumed.set()
            self.dispatch("start")
        return allowed

    def stop(self) -> bool:
        """Stops the fish bowl.

        This will emit a `stop` event unless the fish bowl does
        not need to be stopped, e.g. if the clock is not running.

        Returns:
            bool: True if the fish bowl was stopped, False otherwise.
        """
        allowed = self.is_running()
        if allowed:
            self._alive.clear()
            self.dispatch("stop")
        return allowed

    def is_paused(self):
        """Checks if the fish bowl is paused."""
        return not self._resumed.is_set()

    def is_running(self):
        """Checks if the fish bowl is running."""
        return self._alive.is_set()

    ## SLEEPING MANAGEMENT ############################################################

    async def sleep(self, duration: Union[int, float]):
        """Sleeps for the given duration.

        This method is simply a shorthand for `self.sleeper.sleep(duration)`.
        """
        return await self.sleeper.sleep(duration)

    # Hot-swap methods ############################################################

    def swap_clock(self, clock: "BaseClock"):
        """Hot-swap the current clock for a different clock.

        This method will perform the following procedure:
            1. Pause the fish bowl
            2. Remove the old clock's handler
            3. Replace with the current clock and add as handler
            4. Resume fish bowl
            5. Trigger a `clock_swap` event with one argument, the new clock instance
        """
        self.pause()
        self.remove_handler(self.clock)
        self.clock = clock
        self.add_handler(clock)
        self.resume()
        self.dispatch("clock_swap", clock)
        
    def swap_parser(self, parser: "BaseParser"):
        """Hot-swap the current parser for a different one (eg. base -> ziffers)."""
        self.remove_handler(self.parser)
        self.add_handler(parser)
        self.dispatch("parser_swap", parser)

    ## HANDLERS ############################################################

    def add_handler(self, handler: "BaseHandler"):
        """Adds a new handler to the fish bowl.

        If the handler has any child handlers, they will be
        recursively added to the fish bowl as well.

        This method is idempotent; adding the handler more than once
        will cause nothing to happen. However, handler objects cannot
        be shared across different fish bowls.

        If an error occurs during the handler setup (including its children),
        the handler will be removed before propagating the exception.
        This means that `teardown()` is called even after an incomplete setup.

        Args:
            handler (BaseHandler): The handler being added.

        Raises:
            ValueError:
                The handler is either already added to a different fish bowl
                or the handler's parent was not yet added to this fish bowl.
        """
        if handler.env is not None:
            if handler.env is self:
                return
            raise ValueError(f"{handler!r} was already added to {handler.env!r}")
        elif handler.parent is not None and handler.parent.env is not self:
            if handler.parent.env is None:
                raise ValueError(
                    f"The parent {handler.parent!r} must be added to the fish bowl"
                )
            else:
                raise ValueError(
                    f"The parent {handler.parent!r} was already added to {handler.env!r}"
                )

        # It may be possible that the user set `env` to None, but
        # given that `register_hook()` is idempotent, it's probably
        # fine to call `BaseHandler.setup()` again

        handler._env = self  # pylint: disable=protected-access
        self._handlers[handler] = None
        try:
            handler.setup()
            for child in handler.children:
                self.add_handler(child)
        except BaseException as e:
            self.remove_handler(handler)
            raise e

    def remove_handler(self, handler: "BaseHandler"):
        """Removes an existing handler from the fish bowl.

        If the handler has any child handlers, they will be
        recursively removed from the fish bowl as well.

        After the handler has been removed, it can be re-used in new fish bowls.

        This method is idempotent; removing the handler when
        it has already been removed will cause nothing to happen.

        If an error occurs during the handler teardown (including its children),
        its children and hooks will still be removed. At the end, all exceptions
        are grouped into a `BaseExceptionGroup` before being raised.

        Args:
            handler (BaseHandler): The handler to remove from the fish bowl.

        Raises:
            ValueError:
                One of the handler's parents has locked its children from
                being removed.
        """
        if handler not in self._handlers:
            return
        elif handler.locked:
            raise ValueError(f"{handler!r} has been locked by its parent")

        exceptions: list[BaseException] = []

        was_locked = handler.lock_children
        handler.lock_children = None

        for child in handler.children:
            try:
                self.remove_handler(child)
            except BaseException as e:  # pylint: disable=invalid-name,broad-except
                exceptions.append(e)

        handler.lock_children = was_locked

        try:
            handler.teardown()
        except BaseException as e:  # pylint: disable=invalid-name,broad-except
            exceptions.append(e)

        handler._env = None  # pylint: disable=protected-access
        del self._handlers[handler]

        event_set = self._hook_events.get(handler)
        if event_set is not None:
            for event in tuple(event_set):
                self.unregister_hook(event, handler)

        if exceptions:
            raise BaseExceptionGroup(
                f"Errors raised while removing {handler!r}", exceptions
            )

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
        hook_dict = self._event_hooks[event]
        if hook in hook_dict:
            return

        hook_dict[hook] = None
        self._hook_events[hook][event] = None

    def unregister_hook(self, event: Optional[str], hook: HookProtocol):
        """Unregisters a hook for a specific event.

        Global hooks can be removed by passing `None` as the event.

        This method is idempotent; unregistering a hook that does not
        exist for a given event will cause nothing to happen.

        Args:
            event (Optional[str]): The event to remove the hook from.
            hook (HookProtocol): The hook being removed.
        """
        hook_dict = self._event_hooks.get(event)
        if hook_dict is not None:
            hook_dict.pop(hook, None)
            if not hook_dict:
                del self._event_hooks[event]

        event_dict = self._hook_events.get(hook)
        if event_dict is not None:
            event_dict.pop(event, None)
            if not event_dict:
                del self._hook_events[hook]

    def _run_hooks(self, hooks: Iterable[HookProtocol], event: str, *args):
        # TODO add hook ratelimiting
        exceptions: list[BaseException] = []
        for func in hooks:
            try:
                func(event, *args)

            except Exception as e:  # pylint: disable=invalid-name,broad-except
                exceptions.append(e)
            except BaseException as e:  # pylint: disable=invalid-name,broad-except
                exceptions.append(e)
                break

        if exceptions:
            raise BaseExceptionGroup(
                f"Errors raised while running hooks for {event}", exceptions
            )

    def dispatch(self, event: str, *args):
        """Dispatches an event to it associated hooks with the given arguments.

        Args:
            event (str): The name of the event being dispatched.
            *args: The arguments to pass to the event.
        """
        empty_dict: dict[HookProtocol, None] = {}
        local_hooks = self._event_hooks.get(event, empty_dict)
        global_hooks = self._event_hooks.get(None, empty_dict)

        all_hooks = local_hooks | global_hooks
        self._run_hooks(all_hooks, event, *args)
