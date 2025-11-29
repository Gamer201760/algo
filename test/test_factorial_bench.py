import pytest

from domain.algo.factorial import (
    factorial,
    factorial_recursive,
)


@pytest.mark.benchmark(group='factorial-iter-vs-rec')
@pytest.mark.parametrize('n', [5, 10, 50, 100, 500])
@pytest.mark.parametrize(
    'fn',
    [
        factorial,
        factorial_recursive,
    ],
)
def test_factorial_benchmark(benchmark, fn, n):
    benchmark(fn, n)
