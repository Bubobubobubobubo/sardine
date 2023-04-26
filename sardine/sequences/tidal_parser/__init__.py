from .control import *
from .tidal_euclid import *
from .pattern import *
from .utils import *
from .mini import *
from .stream import SuperDirtStream

__streams = {}

def p(key, pattern=None):
    if key not in __streams:
        __streams[key] = SuperDirtStream(name=key)
        _default_clock.subscribe(__streams[key])
    if pattern:
        __streams[key].pattern = pattern
    return __streams[key]


def hush():
    for stream in __streams.values():
        stream.pattern = silence
        _default_clock.unsubscribe(stream)
    __streams.clear()


class __Streams:
    def __setitem__(self, key, value):
        p(key, value)


d = __Streams()
