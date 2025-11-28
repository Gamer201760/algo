from functools import cmp_to_key
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from _typeshed import SupportsAllComparisons


def heap_sort[T: 'SupportsAllComparisons'](
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

    # работаем с копией исходного списка
    result = list(a)
    n = len(result)

    def sift_down(i: int, size: int) -> None:
        # просеивание элемента вниз в пределах size
        while True:
            left = 2 * i + 1
            right = left + 1
            largest = i

            # выбираем больший ребенок по ключу
            if left < size and key_func(result[left]) > key_func(result[largest]):
                largest = left
            if right < size and key_func(result[right]) > key_func(result[largest]):
                largest = right

            # если текущий элемент уже на своем месте выходим
            if largest == i:
                break

            # меняем местами и продолжаем просеивание
            result[i], result[largest] = result[largest], result[i]
            i = largest

    # строим max heap
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)

    # извлекаем максимумы по одному и уменьшаем кучу
    for end in range(n - 1, 0, -1):
        result[0], result[end] = result[end], result[0]
        sift_down(0, end)

    return result
