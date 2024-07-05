import pytest
from main import cache, slow_function, MyClass, async_function


def test_cache():
    assert slow_function(1) == 1
    assert slow_function(1) == 1
    assert len(cache.data) == 1

    obj = MyClass()
    assert obj.method(1) == 1
    assert obj.method(1) == 1
    assert len(cache.data) == 2

    cache.invalidate(slow_function)
    assert len(cache.data) == 1


@pytest.mark.asyncio
async def test_cache_async():
    # cache все еще хранит результат вызова MyClass.method() в этом месте, если запускать тесты пачкой
    # очистим кеш, вызвав 'invalidate' без параметра
    cache.invalidate()
    assert len(cache.data) == 0
    assert await async_function(1) == 1
    assert await async_function(1) == 1
    assert len(cache.data) == 1

    cache.invalidate(async_function)
    assert len(cache.data) == 0

