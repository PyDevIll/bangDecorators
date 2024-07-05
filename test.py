import pytest
from main import cache, slow_function, MyClass, async_function


def test_cache():
    # cache = Cache()     # без этого объявления pyCharm подозрительно выделяет cache
    assert slow_function(1) == 1
    assert slow_function(1) == 1
    assert len(cache.data) == 1

    obj = MyClass()
    assert obj.method(1) == 1       # TypeError in wrapper: str() parameter 'encoding' must be str, not int
    # assert obj.method(1) == 1
    # assert len(cache.data) == 2
    #
    # cache.invalidate(slow_function)
    # assert len(cache.data) == 1


@pytest.mark.asyncio
async def test_cache_async():
    # cache = Cache()     # без этого объявления pyCharm подозрительно выделяет cache
    assert await async_function(1) == 1
    assert await async_function(1) == 1
    assert len(cache.data) == 1

    cache.invalidate(async_function)
    assert len(cache.data) == 0

