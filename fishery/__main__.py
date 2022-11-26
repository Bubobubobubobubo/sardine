import contextlib
import io
from typing import Optional

import click

try:
    import yappi
except ImportError:
    yappi = None

from . import console


class Profiler:
    def __init__(self, filepath: Optional[str]):
        self.filepath = filepath

    def __enter__(self):
        if self.filepath is None:
            return self
        elif yappi is None:
            raise RuntimeError("yappi must be installed to enable profiling")

        yappi.set_clock_type("WALL")
        yappi.start(builtins=False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.filepath is None:
            return

        yappi.stop()
        ystats = yappi.get_func_stats()
        pstats = yappi.convert2pstats(ystats)
        pstats.dump_stats(self.filepath)
        click.echo(f"Profiler stats written to {self.filepath}")


@click.command()
@click.option(
    "-p", "--profile", "profile_filepath",
    default=None,
    help="Profile sardine in the background and output pstats results "
         "to the given file (requires the yappi package)",
    type=click.Path(dir_okay=False, writable=True),
)
@click.version_option(
    package_name="sardine",
    prog_name=__package__,
    message="%(prog)s for %(package)s v%(version)s",
)
def main(profile_filepath: Optional[io.BufferedWriter]):
    with Profiler(profile_filepath):
        console.start()


if __name__ == "__main__":
    main()
