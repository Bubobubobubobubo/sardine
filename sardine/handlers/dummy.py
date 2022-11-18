from ..base.handler import BaseHandler

__all__ = ("DummyHandler",)


class DummyHandler(BaseHandler):
    def __init__(self, ip: str = "127.0.0.1", port: int = 23456):
        self._ip, self._port = (ip, port)
        self.env = None
        self._events = {
            "bleep": self._bleep,
            "bloop": self._bloop,
        }

    def __repr__(self) -> str:
        return f"OSCHandler: {self._ip}:{self._port}"

    def setup(self):
        for event in self._events:
            self.register(event)

    def hook(self, event: str, *args):
        func = self._events[event]
        func(*args)

    def _bleep(self, *args) -> None:
        print(f"bleep: {args}")

    def _bloop(self, *args) -> None:
        print(f"bloop: {args}")
