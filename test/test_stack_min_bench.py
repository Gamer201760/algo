import random

import pytest

from domain.structures.stack import MinStack

N = 100_000
SEED = 42


def make_filled_stack():
    rng = random.Random(SEED)
    stack = MinStack()
    for _ in range(N):
        stack.push(rng.randint(-1_000_000, 1_000_000))
    return stack


@pytest.mark.benchmark(group='stack-min')
def test_min_stack_benchmark(benchmark):
    stack = make_filled_stack()

    def bench_min():
        return stack.min()

    benchmark(bench_min)


@pytest.mark.benchmark(group='stack-min')
def test_builtin_min_benchmark(benchmark):
    stack = make_filled_stack()

    def bench_min():
        return min(stack._data)

    benchmark(bench_min)
