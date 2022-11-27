from ..base import BaseHandler
from typing import Optional
from osc4py3.as_eventloop import *
import threading
import asyncio
import time

__all__ = ("OscLoop",)

class OscLoop(BaseHandler):

    POLL_INTERVAL = 0.001

    def __init__(self):
        super().__init__()
        self.env = None

        # Thread control
        self._run_thread: Optional[threading.Thread] = None
        self._completed_event = asyncio.Event()
        self._events = {
                'start': lambda: asyncio.create_task(self.run())
        }

    def setup(self):
        for event in self._events:
            self.register(event)

    def hook(self, event: str, *args):
        func = self._events[event]
        func(*args)

    async def run(self):
        """Main Loop for OSC"""
        self._completed_event.clear()
        self._run_thread = threading.Thread(target=self._run)
        self._run_thread.start()

        try:
            await self._completed_event.wait()
        finally:
            self._completed_event.set()

    def _run(self):
        """Low-level loop"""
        osc_startup()
        try:
            while not self._completed_event.is_set():
                osc_process()
                time.sleep(self.POLL_INTERVAL)
        finally:
            osc_terminate()
