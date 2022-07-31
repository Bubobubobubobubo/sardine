from dataclasses import dataclass
from typing import Any, Awaitable

@dataclass
class AsyncRunner:
    function: Awaitable
    last_valid_function: Awaitable
    tasks: list
