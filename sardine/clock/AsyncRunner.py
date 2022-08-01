import asyncio
from dataclasses import dataclass, field
import inspect
import traceback
from typing import Callable, Coroutine, TYPE_CHECKING

if TYPE_CHECKING:
    from .Clock import Clock

CoroFunc = Callable[..., Coroutine]


@dataclass
class FunctionState:
    func: CoroFunc
    args: tuple
    kwargs: dict


@dataclass
class AsyncRunner:
    """Handles calling synchronizing and running a function in
    the background, with support for run-time function patching.

    This class should only be used through a Clock instance via
    the `Clock.schedule()` method.

    """
    clock: "Clock"
    states: list[FunctionState] = field(default_factory=list)

    _swimming: bool = False
    _stop: bool = False
    _task: asyncio.Task | None = None

    def push(self, func: CoroFunc, *args, **kwargs):
        """Pushes a function state to the runner to be called in
        the next iteration."""
        if not self.states or func is not self.states[-1].func:
            return self.states.append(FunctionState(func, args, kwargs))

        # patch the top-most state
        state = self.states[-1]
        state.args = args
        state.kwargs = kwargs

    def start(self):
        """Initializes the background runner task.

        :raises RuntimeError:
            This method was called after the task already started.

        """
        if self._task is not None:
            raise RuntimeError('runner task has already started')

        self.swim()
        self._task = asyncio.create_task(self._runner())
        self._task.add_done_callback(asyncio.Task.result)

    def started(self) -> bool:
        """Returns True if the runner has been started.

        This method will remain true even if the runner stops afterwards.

        """
        return self._task is not None

    def swim(self):
        """Allows the runner to continue the next iteration.
        This method must be called continuously to keep the runner alive."""
        self._swimming = True

    def stop(self):
        """Stops the runner's execution after the current iteration.

        This method takes precedence when `swim()` is also called.

        """
        self._stop = True

    async def _runner(self):
        initial = True
        last_state = self.states[-1]
        name = last_state.func.__name__
        print(f'[Init {name}]')

        while self.states and not self._stop:
            # `state.func` must schedule itself to keep swimming
            self._swimming = False
            state = self.states[-1]
            name = state.func.__name__

            if state is not last_state:
                pushed = len(self.states) > 1 and self.states[-2] is last_state
                print(f'[Reloaded {name}]' if pushed else f'[Restored {name}]')
                last_state = state

            # Introspect arguments to synchronize
            if initial:
                await self._wait(0)
            else:
                delay = state.kwargs.get('delay')
                if delay is None:
                    param = inspect.signature(state.func).parameters.get('delay')
                    delay = getattr(param, 'default', 1)

                await self._wait(delay)

            try:
                await state.func(*state.args, **state.kwargs)
            except asyncio.CancelledError:
                # assume the user has intentionally cancelled
                return
            except Exception as e:
                print(f'Exception encountered in {name}:')
                traceback.print_exception(e)

                self._revert_state()

            initial = False

        # Remove from clock
        print(f'[Stopped {name}]')
        self.clock.runners.pop(name)

    async def _wait(self, delay: float | int):
        clock = self.clock

        if delay == 0:
            cur_bar = clock.elapsed_bars
            while clock.phase != 1 and clock.elapsed_bars != cur_bar + 1:
                await asyncio.sleep(self._wait_resolution)
        else:
            next_time = clock.get_tick_time() + delay * clock.ppqn
            while clock.tick_time < next_time:
                await asyncio.sleep(self._wait_resolution)

    @property
    def _wait_resolution(self):
        # Sleep resolution may be increased here
        return self.clock._get_tick_duration() / (self.clock.ppqn * 2)

    def _revert_state(self):
        failed = self.states.pop()

        if self.states:
            # patch the global scope so recursive functions don't
            # invoke the failed function
            reverted = self.states[-1]
            failed.func.__globals__[failed.func.__name__] = reverted.func
