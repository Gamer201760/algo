from domain.sort.quick import quick_sort


def bucket_sort(
    a: list[float],
    *,
    buckets: int | None = None,
) -> list[float]:
    # обрабатываем пустой список
    if not a:
        return []

    # определяем количество бакетов
    n = len(a)
    bucket_count = buckets if buckets is not None and buckets > 0 else n

    # создаем пустые бакеты
    buckets_list: list[list[float]] = [[] for _ in range(bucket_count)]

    # раскладываем элементы по бакетам
    for x in a:
        if not 0.0 <= x < 1.0:
            raise ValueError(
                'bucket_sort_float ожидает значения в диапазоне от нуля включительно до единицы не включая единицу'
            )
        # вычисляем индекс бакета по формуле int(x * bucket_count)
        idx = int(x * bucket_count)
        if idx == bucket_count:
            idx = bucket_count - 1
        buckets_list[idx].append(x)

    # сортируем каждый бакет встроенной сортировкой и собираем результат
    result: list[float] = []
    for bucket in buckets_list:
        if not bucket:
            continue
        # добавляем отсортированный бакет в результат
        result.extend(quick_sort(bucket))

    return result
