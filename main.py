from functools import wraps
import asyncio


class Cache:
    def __init__(self):
        self.data = {}

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # если в словаре словарей self.data по ключам имени функции и переданным параметрам
            # находится предвычисленное значение - возвращаем его
            key = str(*args) + str(**kwargs)
            if func.__name__ in self.data:
                if key in self.data[func.__name__]:
                    return self.data[func.__name__][key]

            # иначе - вычисляем значение, сохраняем его в data и возвращаем
            result = func(*args, **kwargs)
            if func.__name__ not in self.data:
                self.data[func.__name__] = {}
            self.data[func.__name__][key] = result
            return result

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            ...

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return wrapper

    def invalidate(self, func):
        self.data[func.__name__].clear()


cache = Cache()


@cache
def slow_function(arg):
    print(f"Function 'slow_function' is actually run")
    return arg


class MyClass:
    @cache
    def method(self, arg):
        print(f"Function 'MyClass.method' is actually run")
        return arg


@cache
async def async_function(arg):
    print(f"Function 'async_function' is actually run")
    return arg
