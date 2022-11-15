class Time:
    def __init__(
        self, 
        elapsed_time: float=0.0, 
    ):
        self._elapsed_time = elapsed_time

    def __repr__(self) -> str:
        return f"Started: {self._elapsed_time} seconds ago."

    def reset(self):
        """Reset elasped time"""
        self._elapsed_time = 0.0