from typing import Callable


def counting_sort[T](
    a: list[T],
    *,
    key: Callable[[T], int] | None = None,
) -> list[T]:
    # обрабатываем пустой список
    if not a:
        return []

    if key is None:
        # ветка без key предполагаем что T это int
        keys: list[int] = []
        for x in a:
            if not isinstance(x, int):
                raise TypeError('counting_sort без key поддерживает только list[int]')
            keys.append(x)
    else:
        # ветка с key сразу используем key
        keys = [key(x) for x in a]

    # находим минимум и максимум ключа
    min_key = min(keys)
    max_key = max(keys)

    # считаем смещение
    offset = -min_key
    size = max_key - min_key + 1

    # создаем массив счетчиков
    counts = [0] * size

    # считаем количество каждого ключа
    for k in keys:
        counts[k + offset] += 1

    # строим префиксные суммы
    for i in range(1, size):
        counts[i] += counts[i - 1]

    # создаем список результата
    result: list[T] = [a[0]] * len(a)

    # заполняем результат в обратном порядке для стабильности
    for x, k in zip(reversed(a), reversed(keys)):
        idx = k + offset
        counts[idx] -= 1
        pos = counts[idx]
        result[pos] = x

    return result
