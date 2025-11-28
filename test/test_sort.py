from typing import Counter

import pytest

from domain.sort import (
    bubble_sort,
    bucket_sort,
    counting_sort,
    heap_sort,
    quick_sort,
    radix_sort,
)

from .conftest import (
    many_duplicates,
    nearly_sorted,
    rand_float_array,
    rand_int_array,
    reverse_sorted,
)


@pytest.mark.parametrize(
    'data',
    [
        [],
        rand_float_array(1, seed=1),
        rand_float_array(10, seed=2),
        rand_float_array(100, seed=3),
    ],
)
def test_bucket_sort_valid(data):
    result = bucket_sort(data.copy())
    assert result == sorted(data)


@pytest.mark.parametrize(
    'sort_fn',
    [
        bubble_sort,
        quick_sort,
        heap_sort,
        counting_sort,
        radix_sort,
    ],
)
@pytest.mark.parametrize(
    'data',
    [
        [],
        [1],
        [1, 1, 1],
        reverse_sorted(10),
        nearly_sorted(20, swaps=5, seed=1),
        many_duplicates(50, k_unique=5, seed=2),
        rand_int_array(100, 0, 1_000, seed=3),
    ],
)
def test_int_sorts_valid(sort_fn, data):
    result = sort_fn(data.copy())
    assert result == sorted(data)


@pytest.mark.parametrize(
    'sort_fn',
    [
        bubble_sort,
        quick_sort,
        heap_sort,
        counting_sort,
    ],
)
@pytest.mark.parametrize(
    'data,key',
    [
        ([], None),
        ([1], None),
        ([1, 1, 1], None),
        (reverse_sorted(10), None),
        (nearly_sorted(20, swaps=5, seed=1), None),
        (many_duplicates(50, k_unique=5, seed=2), None),
        (rand_int_array(100, -500, 500, seed=3), None),
        (reverse_sorted(10), abs),
        (rand_int_array(100, -500, 500, seed=4), abs),
        (rand_int_array(100, 0, 500, seed=5), lambda x: x % 10),
    ],
)
def test_int_sorts_key(sort_fn, data, key):
    result = sort_fn(data.copy(), key=key)

    # массивы должны быть перестановками друг друга
    assert Counter(result) == Counter(data)

    # ключи должны быть неубывающими
    k = key or (lambda x: x)
    keys = [k(x) for x in result]
    assert all(keys[i] <= keys[i + 1] for i in range(len(keys) - 1))


@pytest.mark.parametrize(
    'data,key',
    [
        ([], None),
        ([1], None),
        ([1, 1, 1], None),
        (reverse_sorted(10), None),
        (nearly_sorted(20, swaps=5, seed=1), None),
        (many_duplicates(50, k_unique=5, seed=2), None),
        (rand_int_array(100, 0, 500, seed=3), None),
        (reverse_sorted(10), abs),
        (rand_int_array(100, 0, 500, seed=4), abs),
        (rand_int_array(100, 0, 500, seed=5), lambda x: x % 10),
    ],
)
def test_radix_sort_key(data, key):
    expected = sorted(data, key=key)
    result = radix_sort(data.copy(), key=key)
    assert result == expected
