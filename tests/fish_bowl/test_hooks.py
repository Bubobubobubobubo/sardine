from typing import Any, Optional

import pytest
from sardine import BaseHandler, FishBowl

from . import fish_bowl


class DummyHandler(BaseHandler):
    EVENTS = ('foo', 'bar', 'foo')

    def __init__(self):
        super().__init__()
        self.has_setup = False
        self.has_teared_down = False
        self.last_event: Optional[tuple[str, tuple[Any, ...]]] = None
        self.event_count = 0

    def setup(self):
        self.has_setup = True
        for event in self.EVENTS:
            self.register(event)

    def teardown(self):
        self.has_teared_down = True

    def reset_event_count(self):
        self.event_count = 0

    def hook(self, event: str, *args):
        self.last_event = (event, args)
        self.event_count += 1


@pytest.fixture
def dummy_handler() -> DummyHandler:
    return DummyHandler()


def test_handler(fish_bowl: FishBowl, dummy_handler: DummyHandler):
    temp_event = 'baz'

    # Ensure test hooks aren't in use
    for event in dummy_handler.EVENTS + (temp_event,):
        assert fish_bowl._event_hooks.get(event) is None

    # Add handler and check for setup call
    fish_bowl.add_handler(dummy_handler)
    assert dummy_handler.has_setup

    assert dummy_handler.env is fish_bowl

    # Verify installation of hooks
    for event in dummy_handler.EVENTS:
        assert dummy_handler in fish_bowl._event_hooks[event]

    assert fish_bowl._hook_events[dummy_handler] == set(dummy_handler.EVENTS)

    # Test each hook
    for i, event in enumerate(dummy_handler.EVENTS):
        fish_bowl.dispatch(event, i)
        assert dummy_handler.last_event == (event, (i,))

    # Test global hook
    dummy_handler.reset_event_count()
    dummy_handler.register(None)

    fish_bowl.dispatch(temp_event)
    assert dummy_handler.last_event == (temp_event, ())

    # Make sure hooks aren't called twice with existing events
    existing_event = dummy_handler.EVENTS[0]
    fish_bowl.dispatch(existing_event)
    assert dummy_handler.last_event == (existing_event, ())
    assert dummy_handler.event_count == 2

    # Verify removal of hooks
    fish_bowl.remove_handler(dummy_handler)
    assert dummy_handler.has_teared_down

    for event in dummy_handler.EVENTS:
        assert fish_bowl._event_hooks.get(event) is None

    assert fish_bowl._hook_events.get(dummy_handler) is None
