from typing import Literal, Optional

import click

try:
    import yappi
except ImportError:
    yappi = None

__all__ = ("Profiler", "yappi")


class Profiler:
    def __init__(
        self,
        clock: Literal["CPU", "WALL"],
        filepath: str,
    ):
        self.clock = clock
        self.filepath = filepath

    def __enter__(self):
        if yappi is None:
            raise RuntimeError("yappi must be installed to enable profiling")

        yappi.set_clock_type(self.clock)
        yappi.start(builtins=False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        yappi.stop()
        ystats = yappi.get_func_stats()
        pstats = yappi.convert2pstats(ystats)
        pstats.dump_stats(self.filepath)
        click.echo(f"Profiler stats written to {self.filepath}")
