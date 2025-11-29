from functools import lru_cache


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError('Факториал поддерживает только положительные n')

    result = 1
    for k in range(2, n + 1):
        result *= k
    return result


def factorial_recursive(n: int) -> int:
    if n < 0:
        raise ValueError('Факториал поддерживает только положительные n')
    if n in (0, 1):
        return 1
    return n * factorial_recursive(n - 1)


@lru_cache(None)
def factorial_recursive_cache(n: int) -> int:
    if n < 0:
        raise ValueError('Факториал поддерживает только положительные n')
    if n in (0, 1):
        return 1
    return n * factorial_recursive(n - 1)
