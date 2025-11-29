import pytest

from domain.algo.fib import fibo, fibo_recursive


@pytest.mark.parametrize(
    'n, expected',
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
    ],
)
def test_fibo_iterative(n: int, expected: int) -> None:
    assert fibo(n) == expected


@pytest.mark.parametrize('n', [0, 1, 2, 3, 4, 5, 6, 10])
def test_fibo_recursive_matches_iterative(n: int) -> None:
    assert fibo_recursive(n) == fibo(n)


@pytest.mark.parametrize('n', [-1, -3])
def test_fibo_negative_raises(n: int) -> None:
    with pytest.raises(ValueError):
        fibo(n)
    with pytest.raises(ValueError):
        fibo_recursive(n)
