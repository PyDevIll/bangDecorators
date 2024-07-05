from functools import wraps
import asyncio


class Cache:
    def __init(self):
        self.data = {}

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ...

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            ...

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return wrapper

    def invalidate(self, func):
        ...


cache = Cache()


@cache
def slow_function(arg):
    print("Calculating...")
    return arg


class MyClass:
    @cache
    def method(self, arg):
        print("Calculating...")
        return arg


@cache
async def async_function(arg):
    return arg

