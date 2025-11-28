from functools import cmp_to_key
from typing import Any, Callable

from _typeshed import SupportsAllComparisons


def bubble_sort[T: SupportsAllComparisons](
    a: list[T],
    *,
    key: Callable[[T], Any] | None = None,
    cmp: Callable[[T, T], int] | None = None,
) -> list[T]:
    # проверяем что не переданы обе функции сразу

    if cmp is not None:
        if key is not None:
            raise ValueError('Используйте или key или cmp')
        key_func = cmp_to_key(cmp)
    else:
        key_func = key or (lambda x: x)

    # создаем копию списка чтобы не менять входные данные
    result = list(a)
    n = len(result)

    # основной цикл пузырьковой сортировки
    for i in range(n):
        swapped = False
        # каждый проход отправляет самый большой элемент в конец
        for j in range(0, n - 1 - i):
            if key_func(result[j]) > key_func(result[j + 1]):
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        # если обменов не было список уже отсортирован
        if not swapped:
            break

    return result
