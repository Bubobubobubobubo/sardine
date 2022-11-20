import asyncio
import collections
from typing import Hashable, Iterable, Optional, Protocol, Union

from exceptiongroup import BaseExceptionGroup

from .scheduler import Scheduler
from .base import BaseClock, BaseHandler, BaseParser
from .clock import Time, InternalClock
from .handlers import SleepHandler
from .sequences.SardineParser.ListParser import ListParser
from .sequences.Iterators import Iterator
from .sequences.Variables import Variables
from .sequences.patterns import Pattern

__all__ = ("FishBowl",)


class HookProtocol(Hashable, Protocol):
    """A callable object that accepts an event and any number of arguments."""

    def __call__(self, event: str, *args):
        ...


class FishBowl:
    """Contains all the components necessary to run the Sardine system."""

    def __init__(
        self,
        clock: BaseClock = None,
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

    ## REPR/STR #######################################################################

    def __repr__(self) -> str:

        # Basic attributes
        alv, set = self._alive.is_set(), self._resumed.is_set()
        tp, bt = self.clock.tempo, self.clock.beat
        hn = [type(handler).__name__ for handler in self._handlers]

        return f"<Bowl alive={alv} playing={set} tempo={tp} beat={bt} handlers={hn}>"

    ## TRANSPORT ######################################################################

    def pause(self):
        """Pauses the fish bowl.

        This will emit a `pause` event unless the fish bowl does
        not need to be paused, e.g. being paused once already or not
        having started.
        """
        if self.is_running() and not self.is_paused():
            self._resumed.clear()
            self.dispatch("pause")

    def resume(self):
        """Resumes the fish bowl.

        This will emit a `resume` event unless the fish bowl does
        not need to be resumed, e.g. if the clock is not running
        or has not been paused.
        """
        if self.is_running() and self.is_paused():
            self._resumed.set()
            self.dispatch("resume")

    def start(self):
        """Starts the fish bowl.

        This will emit a `start` event unless the fish bowl does
        not need to be started, e.g. if the fish bowl has already started.

        If the fish bowl is started, paused, stopped, and started again,
        handlers should treat it as if the fish bowl is no longer paused.
        """
        if not self.is_running():
            self._alive.set()
            self._resumed.set()
            self.dispatch("start")

    def stop(self):
        """Stops the fish bowl.

        This will emit a `stop` event unless the fish bowl does
        not need to be stopped, e.g. if the clock is not running.
        """
        if self.is_running():
            self._alive.clear()
            self.dispatch("stop")

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

    ## HANDLERS ############################################################

    def add_handler(self, handler: "BaseHandler"):
        """Adds a new handler to the fish bowl.

        This handler will receive all messages currently dispatched
        in the environment and react accordingly.

        This method is idempotent; adding the handler more than once
        will cause nothing to happen. However, handler objects cannot
        be shared across different fish bowls.

        Args:
            handler (BaseHandler): The handler being added.

        Raises:
            ValueError:
                The handler has already been added to a different fish bowl.
        """
        if handler.env is not None:
            if handler.env is self:
                return
            raise ValueError(
                f"{handler!r} is already being used by {handler.env!r}"
            )

        # It may be possible that the user set `env` to None, but
        # given that `register_hook()` is idempotent, it's probably
        # fine to call `BaseHandler.setup()` again

        handler._env = self  # pylint: disable=protected-access
        handler.setup()
        self._handlers[handler] = None

    def remove_handler(self, handler: "BaseHandler"):
        """Removes an existing handler from the fish bowl.

        After a handler has been removed, it can be re-used in new fish bowls.

        This method is idempotent; removing the handler when
        it has already been removed will cause nothing to happen.

        Args:
            handler (BaseHandler): The handler to remove from the fish bowl.
        """
        if handler not in self._handlers:
            return

        handler.teardown()
        handler._env = None  # pylint: disable=protected-access
        del self._handlers[handler]

        event_set = self._hook_events.get(handler)
        if event_set is not None:
            for event in tuple(event_set):
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
            # pylint: disable=invalid-name,broad-except
            except Exception as e:
                exceptions.append(e)
            except BaseException as e:
                exceptions.append(e)
                break
            # pylint: enable=invalid-name,broad-except

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

    def __call__(self, sender_type: str = 'midi', *args, **kwargs) -> Pattern:
        return Pattern()