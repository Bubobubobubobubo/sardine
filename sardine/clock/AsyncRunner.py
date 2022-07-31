from dataclasses import dataclass
from typing import Awaitable

@dataclass
class AsyncRunner:
    function: Awaitable
    function_save: Awaitable
    last_valid_function: Awaitable
