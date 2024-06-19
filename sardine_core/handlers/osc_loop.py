import asyncio

from osc4py3.as_eventloop import osc_process, osc_startup, osc_terminate

from sardine_core.base import BaseRunnerHandler

__all__ = ("OSCLoop",)


class OSCLoop(BaseRunnerHandler):
    def __init__(self, *args, loop_interval: float = 0.001, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop_interval = loop_interval

    async def run(self):
        osc_startup()
        try:
            while True:
                osc_process()
                await asyncio.sleep(self.loop_interval)
        finally:
            osc_terminate()
