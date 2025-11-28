from functools import cmp_to_key
from typing import Counter

import pytest

from domain.sort import bubble_sort, heap_sort, quick_sort

from .conftest import (
    many_duplicates,
    nearly_sorted,
    rand_int_array,
    reverse_sorted,
)


def cmp_asc(a: int, b: int) -> int:
    return (a > b) - (a < b)


def cmp_desc(a: int, b: int) -> int:
    return (b > a) - (b < a)


def cmp_abs(a: int, b: int) -> int:
    return (abs(a) > abs(b)) - (abs(a) < abs(b))


def cmp_mod10(a: int, b: int) -> int:
    a10 = a % 10
    b10 = b % 10
    return (a10 > b10) - (a10 < b10)


@pytest.mark.parametrize(
    'sort_fn',
    [
        bubble_sort,
        quick_sort,
        heap_sort,
    ],
)
@pytest.mark.parametrize(
    'data,cmp',
    [
        ([], cmp_asc),
        ([1], cmp_asc),
        ([1, 1, 1], cmp_asc),
        (reverse_sorted(10), cmp_asc),
        (reverse_sorted(10), cmp_desc),
        (nearly_sorted(20, swaps=5, seed=1), cmp_asc),
        (many_duplicates(50, k_unique=5, seed=2), cmp_asc),
        (rand_int_array(100, -500, 500, seed=3), cmp_asc),
        (rand_int_array(100, -500, 500, seed=4), cmp_abs),
        (rand_int_array(100, 0, 500, seed=5), cmp_mod10),
    ],
)
def test_int_sorts_cmp(sort_fn, data, cmp):
    result = sort_fn(data.copy(), cmp=cmp)

    # результат должен быть перестановкой исходного массива
    assert Counter(result) == Counter(data)

    # последовательность должна быть неубывающей относительно cmp
    for x, y in zip(result, result[1:]):
        assert cmp(x, y) <= 0

    expected = sorted(data, key=cmp_to_key(cmp))
    assert [cmp_to_key(cmp)(x) for x in result] == [
        cmp_to_key(cmp)(x) for x in expected
    ]


@pytest.mark.parametrize(
    'sort_fn',
    [
        bubble_sort,
        quick_sort,
        heap_sort,
    ],
)
def test_int_sorts_key_and_cmp_forbidden(sort_fn):
    data = rand_int_array(10, -10, 10, seed=42)

    with pytest.raises(ValueError):
        sort_fn(data, key=abs, cmp=cmp_asc)
