from functools import wraps
import asyncio


class Cache:
    def __init__(self):
        self.data = {}

    def __get_cached(self, func_name, arg_key):
        if func_name in self.data:
            if arg_key in self.data[func_name]:
                return self.data[func_name][arg_key]
        return None

    def __cache_it(self, result, func_name, arg_key):
        if func_name not in self.data:
            self.data[func_name] = {}
        self.data[func_name][arg_key] = result
        return result

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)

            result = self.__get_cached(func.__name__, key)

            if not result:
                result = func(*args, **kwargs)
                self.__cache_it(result, func.__name__, key)

            return result

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # не хочется повторять код из синхронного wrapper'а
            # нарушается принцип DRY
            # попробуем выделить общий код в отдельную ф-ию
            ...

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return wrapper

    def invalidate(self, func):
        del self.data[func.__name__]


cache = Cache()


@cache
def slow_function(arg):
    print(f"\nFunction 'slow_function' is actually run")
    return arg


class MyClass:
    @cache
    def method(self, arg):
        print(f"\nFunction 'MyClass.method' is actually run")
        return arg


@cache
async def async_function(arg):
    print(f"\nFunction 'async_function' is actually run")
    return arg
