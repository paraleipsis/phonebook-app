import asyncio
from functools import wraps
from typing import Awaitable


def coro(f: Awaitable) -> callable:
    """
    Wrapper to run coroutine (async func) in asyncio event loop.

    :param f:
        Coroutine to run.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper
