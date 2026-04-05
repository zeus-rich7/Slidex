from concurrent.futures import ThreadPoolExecutor
from functools import wraps, partial
from typing import Callable, TypeVar, Coroutine, Any
import asyncio

F = TypeVar("F", bound=Callable[..., Any])


class to_async:  # noqa: N801
    def __init__(self, *, executor: ThreadPoolExecutor | None = None):
        self.executor = executor

    def __call__(self, blocking: F) -> Callable[..., Coroutine[Any, Any, Any]]:
        @wraps(blocking)
        async def wrapper(*args, **kwargs):
            loop = asyncio.get_event_loop()
            if not self.executor:
                self.executor = ThreadPoolExecutor()
            func = partial(blocking, *args, **kwargs)
            return await loop.run_in_executor(self.executor, func)
        return wrapper  # type: ignore[return-value]