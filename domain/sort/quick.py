from functools import cmp_to_key
from typing import Any, Callable

from _typeshed import SupportsAllComparisons


def quick_sort[T: SupportsAllComparisons](
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

    # создаем копию списка чтобы не менять исходный
    result = list(a)

    def _quick_sort(left: int, right: int) -> None:
        # базовый случай когда подмассив короткий
        if left >= right:
            return

        # выбираем опорный элемент как середину отрезка
        pivot = key_func(result[(left + right) // 2])
        i = left
        j = right

        # двигаем указатели навстречу относительно pivot
        while i <= j:
            while key_func(result[i]) < pivot:
                i += 1
            while key_func(result[j]) > pivot:
                j -= 1
            if i <= j:
                result[i], result[j] = result[j], result[i]
                i += 1
                j -= 1

        # рекурсивно сортируем левую и правую части
        if left < j:
            _quick_sort(left, j)
        if i < right:
            _quick_sort(i, right)

    if result:
        _quick_sort(0, len(result) - 1)

    return result
