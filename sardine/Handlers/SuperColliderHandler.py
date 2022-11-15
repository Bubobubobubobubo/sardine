from typing import TYPE_CHECKING
from ..Components.BaseHandler import BaseHandler

if TYPE_CHECKING:
    from ..clock.FishBowl import FishBowl

class SuperColliderHandler(BaseHandler):
    def __init__(self):
        pass

    def setup(self, env: 'FishBowl'):
        pass

    def hook(self, event: str, *args, **kwargs):
        pass