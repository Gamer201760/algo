import pytest

from domain.algo.fib import fibo, fibo_recursive, 



@pytest.mark.benchmark(group='fibo-iter-vs-rec')
@pytest.mark.parametrize('n', [5, 10, 20, 30])
@pytest.mark.parametrize(
    'fn',
    [
        fibo,
        fibo_recursive,
    ],
)
def test_fibo_benchmark(benchmark, fn, n):
    benchmark(fn, n)
