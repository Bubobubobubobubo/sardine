import pytest_asyncio
from sardine import FishBowl


@pytest_asyncio.fixture
def fish_bowl() -> FishBowl:
    return FishBowl()
