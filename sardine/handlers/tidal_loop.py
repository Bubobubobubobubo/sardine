import asyncio

from osc4py3.as_eventloop import osc_process, osc_startup, osc_terminate

from ..base import BaseRunnerHandler

__all__ = ("TidalLoop",)


class TidalLoop(BaseRunnerHandler):
    def __init__(self, *args, loop_interval: float = 0.001, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop_interval = loop_interval

    async def run(self):
        try:
            while True:
                self.env.clock._notify_tidal_streams()
                await asyncio.sleep(self.loop_interval)
        finally:
            pass
