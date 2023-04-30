import asyncio

from osc4py3.as_eventloop import osc_process, osc_startup, osc_terminate

from ..base import BaseRunnerHandler

__all__ = ("TidalLoop",)


class TidalLoop(BaseRunnerHandler):
    def __init__(self, *args, loop_interval: float = 0.05, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop_interval = loop_interval

    async def run(self):
        try:
            while True:
                target_time = self.loop_interval + (
                        self.env.clock._link.clock().micros() / 1e+6)
                self.env.clock._notify_tidal_streams()
                await asyncio.sleep(target_time - self.env.clock._link.clock().micros() / 1e+6)
        finally:
            pass
