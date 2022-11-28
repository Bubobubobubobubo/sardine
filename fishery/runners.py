# Modified copy of asyncio/runners.py from Python 3.11.0
# https://github.com/python/cpython/blob/3.11/Lib/asyncio/runners.py

__all__ = ("Runner",)

import asyncio
import contextvars
import enum
import functools
import signal
import sys
import threading
from typing import Optional


class _State(enum.Enum):
    CREATED = "created"
    INITIALIZED = "initialized"
    CLOSED = "closed"


class Runner:
    """A context manager that controls event loop life cycle.

    The context manager always creates a new event loop,
    allows to run async functions inside it,
    and properly finalizes the loop at the context manager exit.

    If debug is True, the event loop will be run in debug mode.
    If loop_factory is passed, it is used for new event loop creation.

    asyncio.run(main(), debug=True)

    is a shortcut for

    with asyncio.Runner(debug=True) as runner:
        runner.run(main())

    The run() method can be called multiple times within the runner's context.

    This can be useful for interactive console (e.g. IPython),
    unittest runners, console tools, -- everywhere when async code
    is called from existing sync framework and where the preferred single
    asyncio.run() call doesn't work.

    """

    # Note: the class is final, it is not intended for inheritance.

    def __init__(self, *, loop: asyncio.BaseEventLoop, debug: Optional[bool] = None):
        # fishery: instead of a loop_factory argument, we're passing the loop directly
        self._state = _State.CREATED
        self._debug = debug
        self._loop = loop
        self._context = None
        self._interrupt_count = 0
        self._set_event_loop = False

    def __enter__(self):
        self._lazy_init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Shutdown and close event loop."""
        if self._state is not _State.INITIALIZED:
            return
        try:
            loop = self._loop
            _cancel_all_tasks(loop)
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.run_until_complete(loop.shutdown_default_executor())
        finally:
            if self._set_event_loop:
                asyncio.set_event_loop(None)
            loop.close()
            self._loop = None
            self._state = _State.CLOSED

    def get_loop(self):
        """Return embedded event loop."""
        self._lazy_init()
        return self._loop

    def run(self, coro, *, context=None):
        """Run a coroutine inside the embedded event loop."""
        if not asyncio.iscoroutine(coro):
            raise ValueError("a coroutine was expected, got {!r}".format(coro))

        if asyncio._get_running_loop() is not None:
            # fail fast with short traceback
            raise RuntimeError(
                "Runner.run() cannot be called from a running event loop"
            )

        self._lazy_init()

        if context is None:
            context = self._context

        if sys.version_info >= (3, 11):
            task = self._loop.create_task(coro, context=context)
        else:
            task = self._loop.create_task(coro)

        if (
            threading.current_thread() is threading.main_thread()
            and signal.getsignal(signal.SIGINT) is signal.default_int_handler
        ):
            sigint_handler = functools.partial(self._on_sigint, main_task=task)
            try:
                signal.signal(signal.SIGINT, sigint_handler)
            except ValueError:
                # `signal.signal` may throw if `threading.main_thread` does
                # not support signals (e.g. embedded interpreter with signals
                # not registered - see gh-91880)
                sigint_handler = None
        else:
            sigint_handler = None

        self._interrupt_count = 0
        try:
            return self._loop.run_until_complete(task)
        except asyncio.CancelledError:
            if self._interrupt_count > 0:
                uncancel = getattr(task, "uncancel", None)
                # fishery: we do want KeyboardInterrupt propagated on lower versions
                # if uncancel is not None and uncancel() == 0:
                if uncancel is None or uncancel() == 0:
                    raise KeyboardInterrupt()
            raise  # CancelledError
        finally:
            if (
                sigint_handler is not None
                and signal.getsignal(signal.SIGINT) is sigint_handler
            ):
                signal.signal(signal.SIGINT, signal.default_int_handler)

    def _lazy_init(self):
        if self._state is _State.CLOSED:
            raise RuntimeError("Runner is closed")
        if self._state is _State.INITIALIZED:
            return

        # if self._loop_factory is None:
        #     self._loop = asyncio.new_event_loop()
        #     if not self._set_event_loop:
        #         # Call set_event_loop only once to avoid calling
        #         # attach_loop multiple times on child watchers
        #         asyncio.set_event_loop(self._loop)
        #         self._set_event_loop = True
        # else:
        #     self._loop = self._loop_factory()
        asyncio.set_event_loop(self._loop)

        if self._debug is not None:
            self._loop.set_debug(self._debug)
        self._context = contextvars.copy_context()
        self._state = _State.INITIALIZED

    def _on_sigint(self, signum, frame, main_task):
        self._interrupt_count += 1
        if self._interrupt_count == 1 and not main_task.done():
            main_task.cancel()
            # wakeup loop if it is blocked by select() with long timeout
            self._loop.call_soon_threadsafe(lambda: None)
            return
        raise KeyboardInterrupt()


def _cancel_all_tasks(loop: asyncio.BaseEventLoop):
    to_cancel = asyncio.all_tasks(loop)
    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(asyncio.gather(*to_cancel, return_exceptions=True))

    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler(
                {
                    "message": "unhandled exception during asyncio.run() shutdown",
                    "exception": task.exception(),
                    "task": task,
                }
            )
