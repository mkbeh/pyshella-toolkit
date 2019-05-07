# -*- coding: utf-8 -*-
import aiofiles
from functools import wraps


def write(file):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with aiofiles.open(file, 'a') as f:
                async for data in func(*args, **kwargs):
                    await f.write(data)

        return wrapper
    return decorator
