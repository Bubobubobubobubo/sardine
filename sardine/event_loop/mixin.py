import time

__all__ = ("PerfCounterMixin",)


class PerfCounterMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._clock_resolution = time.get_clock_info("perf_counter").resolution

    def time(self) -> float:
        return time.perf_counter()