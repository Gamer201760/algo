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

SORT_FUNCS = [
    ('builtin_sorted', sorted),
    ('bubble_sort', bubble_sort),
    ('quick_sort', quick_sort),
    ('heap_sort', heap_sort),
    ('counting_sort', counting_sort),
]


DATASETS = [
    ('nearly_1k', lambda: nearly_sorted(1_000, swaps=10, seed=1)),
    ('reverse_1k', lambda: reverse_sorted(1_000)),
    ('random_1k', lambda: rand_int_array(1_000, -10_000, 10_000, seed=2)),
    ('dups_1k', lambda: many_duplicates(1_000, k_unique=20, seed=3)),
]


@pytest.mark.benchmark(group='int_sorts')
@pytest.mark.parametrize('dataset_name,make_data', DATASETS)
@pytest.mark.parametrize('name,sort_fn', SORT_FUNCS)
def test_sort_benchmark_ints(benchmark, dataset_name, make_data, name, sort_fn):
    data = make_data()

    def run():
        sort_fn(data.copy())

    benchmark.group = f'{dataset_name}'
    benchmark.name = name

    benchmark(run)


BUCKET_DATASETS = [
    ('random_1k', lambda: rand_float_array(1_000, seed=20)),
    ('random_10k', lambda: rand_float_array(10_000, seed=21)),
    ('random_100k', lambda: rand_float_array(100_000, seed=22)),
]


@pytest.mark.benchmark(group='bucket_sort')
@pytest.mark.parametrize('dataset_name,make_data', BUCKET_DATASETS)
def test_bucket_sort_float_benchmark(benchmark, dataset_name, make_data):
    data = make_data()

    def run():
        bucket_sort(data.copy())

    benchmark.group = f'bucket_sort_{dataset_name}'
    benchmark.name = 'bucket_sort'
    benchmark(run)


@pytest.mark.benchmark(group='bucket_sort')
@pytest.mark.parametrize('dataset_name,make_data', BUCKET_DATASETS)
def test_builtin_sorted_float_benchmark(benchmark, dataset_name, make_data):
    data = make_data()

    def run():
        sorted(data)

    benchmark.group = f'bucket_sort_{dataset_name}'
    benchmark.name = 'builtin_sorted'
    benchmark(run)


RADIX_DATASETS = [
    ('nearly_1k', lambda: nearly_sorted(1_000, swaps=10, seed=10)),
    ('reverse_1k', lambda: reverse_sorted(1_000)),
    ('random_1k', lambda: rand_int_array(1_000, 0, 10_000, seed=11)),
    ('dups_1k', lambda: many_duplicates(1_000, k_unique=20, seed=12)),
    ('random_10k', lambda: rand_int_array(10_000, 0, 1_000_000, seed=13)),
]


@pytest.mark.benchmark(group='radix_sort_int')
@pytest.mark.parametrize('dataset_name,make_data', RADIX_DATASETS)
def test_radix_sort_benchmark(benchmark, dataset_name, make_data):
    data = make_data()

    def run():
        radix_sort(data.copy())

    benchmark.group = f'radix_{dataset_name}'
    benchmark.name = 'radix_sort'
    benchmark(run)


@pytest.mark.benchmark(group='radix_sort_int')
@pytest.mark.parametrize('dataset_name,make_data', RADIX_DATASETS)
def test_builtin_sort_nonnegative_benchmark(benchmark, dataset_name, make_data):
    data = make_data()

    def run():
        radix_sort(data.copy())

    benchmark.group = f'radix_{dataset_name}'
    benchmark.name = 'builtin_sorted'
    benchmark(run)
