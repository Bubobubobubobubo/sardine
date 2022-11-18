from typing import Collection, Optional

import pytest
import pytest_asyncio
from sardine import BaseHandler, FishBowl


@pytest_asyncio.fixture
def fish_bowl():
    return FishBowl()


class EventLoggingHandler(BaseHandler):
    def __init__(self, whitelist: Optional[Collection[str]] = None):
        super().__init__()
        self.whitelist = whitelist
        self.events = []

    def setup(self):
        if self.whitelist is not None:
            for event in self.whitelist:
                self.register(event)
        else:
            self.register(None)

    def hook(self, event: str, *args):
        self.events.append((event, args))


@pytest.mark.asyncio
async def test_transports(fish_bowl: FishBowl):
    logger = EventLoggingHandler(("start", "stop", "pause", "resume"))
    fish_bowl.add_handler(logger)

    # No-ops
    fish_bowl.stop()
    fish_bowl.pause()
    fish_bowl.resume()

    # Regular
    fish_bowl.start()
    fish_bowl.pause()
    fish_bowl.stop()

    fish_bowl.start()
    fish_bowl.resume()  # no-op
    fish_bowl.pause()
    fish_bowl.stop()

    assert logger.events == [
        (event, ()) for event in (
            "start", "pause", "stop",
            "start", "pause", "stop",
        )
    ]
