from dataclasses import dataclass
from typing import Any

@dataclass
class AsyncRunner:
    function: Any
    tasks: list
