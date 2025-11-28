from typing import Callable


def radix_sort[T](
    a: list[T],
    *,
    base: int = 10,
    key: Callable[[T], int] | None = None,
) -> list[T]:
    # обрабатываем пустой список
    if not a:
        return []

    # проверяем основание системы счисления
    if base <= 1:
        raise ValueError('base must be greater than one')

    # подготавливаем функцию целочисленного ключа
    if key is None:

        def key_func(x: T) -> int:
            value = x
            if not isinstance(value, int):
                raise TypeError(
                    'radix_sort требует целые элементы или key возвращающий int'
                )
            return value
    else:

        def key_func(x: T) -> int:
            value = key(x)
            if not isinstance(value, int):
                raise TypeError('key должен возвращать int')
            return value

    # вычисляем ключи для поиска максимального значения
    keys = [key_func(x) for x in a]

    # пока поддерживаем только неотрицательные ключи
    if any(k < 0 for k in keys):
        raise ValueError('radix_sort поддерживает только неотрицательные целые ключи')

    max_key = max(keys)

    # работаем с копией списка
    result = list(a)

    exp = 1

    # пока есть разряды в максимальном ключе
    while max_key // exp > 0:
        # массив счетчиков по текущему разряду
        counts = [0] * base

        # считаем количество каждой цифры
        for x in result:
            digit = (key_func(x) // exp) % base
            counts[digit] += 1

        # строим префиксные суммы для стабильности
        for i in range(1, base):
            counts[i] += counts[i - 1]

        # собираем новый список по текущему разряду
        output: list[T] = [result[0]] * len(result)

        # идем в обратном порядке чтобы сохранить стабильность
        for x in reversed(result):
            digit = (key_func(x) // exp) % base
            counts[digit] -= 1
            pos = counts[digit]
            output[pos] = x

        result = output
        exp *= base

    return result
