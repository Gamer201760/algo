import pytest

from domain.algo.factorial import (
    factorial,
    factorial_recursive,
    factorial_recursive_cache,
)


@pytest.fixture(autouse=True)
def clear_factorial_cache():
    factorial_recursive_cache.cache_clear()
    yield


@pytest.mark.benchmark(group='factorial-iter-vs-rec')
@pytest.mark.parametrize('n', [5, 10, 50, 100, 500])
@pytest.mark.parametrize(
    'fn',
    [
        factorial,
        factorial_recursive,
        factorial_recursive_cache,
    ],
)
def test_factorial_benchmark(benchmark, fn, n):
    benchmark(fn, n)
