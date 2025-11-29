from math import factorial as builtin_factorial

import pytest

from domain.algo.factorial import factorial, factorial_recursive


@pytest.mark.parametrize(
    'n, expected',
    [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 6),
        (4, 24),
        (5, 120),
        (6, 720),
    ],
)
def test_factorial_iterative(n: int, expected: int) -> None:
    assert factorial(n) == expected


@pytest.mark.parametrize('n', [0, 1, 2, 3, 4, 5, 6, 10])
def test_factorial_recursive_matches_iterative(n: int) -> None:
    assert factorial_recursive(n) == factorial(n) == builtin_factorial(n)


@pytest.mark.parametrize('n', [-1, -5])
def test_factorial_negative_raises(n: int) -> None:
    with pytest.raises(ValueError):
        factorial(n)
    with pytest.raises(ValueError):
        factorial_recursive(n)
