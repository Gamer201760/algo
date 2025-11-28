import random


def _rng(seed: int | None) -> random.Random:
    return random.Random(seed)


def rand_int_array(
    n: int,
    lo: int,
    hi: int,
    *,
    distinct: bool = False,
    seed: int | None = None,
) -> list[int]:
    """Случайный список целых чисел"""
    rng = _rng(seed)
    if distinct:
        if hi - lo + 1 < n:
            raise ValueError('диапазон [lo, hi] слишком мал для distinct=True')
        return rng.sample(range(lo, hi + 1), k=n)
    return [rng.randint(lo, hi) for _ in range(n)]


def nearly_sorted(
    n: int,
    swaps: int,
    *,
    seed: int | None = None,
) -> list[int]:
    """Почти отсортированный список с заданным числом свапов"""
    if swaps < 0:
        raise ValueError('swaps должно быть неотрицательным')
    a = list(range(n))
    rng = _rng(seed)
    for _ in range(swaps):
        i = rng.randrange(n) if n > 0 else 0
        j = rng.randrange(n) if n > 0 else 0
        if n > 0:
            a[i], a[j] = a[j], a[i]
    return a


def many_duplicates(
    n: int,
    k_unique: int = 5,
    *,
    seed: int | None = None,
) -> list[int]:
    """Список с большим числом повторяющихся значений"""
    if k_unique <= 0:
        raise ValueError('k_unique должно быть положительным')
    rng = _rng(seed)
    return [rng.randrange(k_unique) for _ in range(n)]


def reverse_sorted(n: int) -> list[int]:
    """Убывающий список от n-1 до 0"""
    return list(range(n - 1, -1, -1))


def rand_float_array(
    n: int,
    lo: float = 0.0,
    hi: float = 1.0,
    *,
    seed: int | None = None,
) -> list[float]:
    """Случайный список чисел с плавающей точкой"""
    if hi < lo:
        raise ValueError('hi должно быть не меньше lo')
    rng = _rng(seed)
    return [rng.uniform(lo, hi) for _ in range(n)]
