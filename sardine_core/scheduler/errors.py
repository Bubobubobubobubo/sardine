class SchedulerError(Exception):
    """An error associated with the scheduler and its async runners."""


class BadFunctionError(SchedulerError):
    """A function pushed to the runner was unacceptable for execution."""


class BadArgumentError(BadFunctionError):
    """The arguments being given to the function were not acceptable."""


class BadPeriodError(BadFunctionError):
    """The period for a given function was not valid."""
