#!/usr/bin/env python3
import questionary
from questionary import Choice, Separator, Style

# ================== Алгоритмы (заглушки / примеры) ==================


def fib(n: int) -> int:
    """Итеративный Fibonacci."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibrec(n: int) -> int:
    """Рекурсивный Fibonacci (наивный)."""
    if n <= 1:
        return n
    return fibrec(n - 1) + fibrec(n - 2)


def fib01(n: int) -> int:
    """Пример «третьего» варианта Fibonacci — через DP."""
    if n <= 1:
        return n
    dp = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def factorial(n: int) -> int:
    """Итеративный факториал."""
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


def factorialrec(n: int) -> int:
    """Рекурсивный факториал."""
    if n <= 1:
        return 1
    return n * factorialrec(n - 1)


def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


# Остальные можно добить позже — сейчас просто заглушки
def counting_sort(arr):
    raise NotImplementedError('counting_sort ещё не реализован')


def heap_sort(arr):
    raise NotImplementedError('heap_sort ещё не реализован')


def radix_sort(arr):
    raise NotImplementedError('radix_sort ещё не реализован')


def bucket_sort(arr):
    raise NotImplementedError('bucket_sort ещё не реализован')


ALGO_FUNCS = {
    'fib': fib,
    'fibrec': fibrec,
    'Fib01': fib01,
    'factorial': factorial,
    'factorialrec': factorialrec,
}

SORT_FUNCS = {
    'bubble': bubble_sort,
    'quick': quick_sort,
    'counting': counting_sort,
    'heap': heap_sort,
    'radix': radix_sort,
    'bucket': bucket_sort,
}


# ================== Стиль Questionary ==================

custom_style = Style(
    [
        ('qmark', 'fg:#00ff7f bold'),  # знак вопроса
        ('question', 'bold'),  # текст вопроса
        ('answer', 'fg:#ffb86c bold'),  # введённый / выбранный ответ
        ('pointer', 'fg:#00ff7f bold'),  # стрелка выбора
        ('highlighted', 'fg:#00ff7f bold'),
        ('selected', 'fg:#00ff7f bold'),
        ('separator', 'fg:#444444'),
        ('instruction', 'fg:#888888'),
    ]
)


# ================== Хелперы ввода ==================


def ask_int(message: str, min_value: int | None = None) -> int:
    def _validate(text: str):
        if not text.strip().lstrip('-').isdigit():
            return 'Нужно целое число'
        value = int(text)
        if min_value is not None and value < min_value:
            return f'Число должно быть ≥ {min_value}'
        return True

    raw = questionary.text(message, validate=_validate, style=custom_style).ask()
    return int(raw)


def ask_array(default_sample: bool = True) -> list[int]:
    use_default = questionary.confirm(
        'Использовать тестовый массив [1, 3, -1, 2, 8, 7, 3, 5]?',
        default=default_sample,
        style=custom_style,
    ).ask()

    if use_default:
        return [1, 3, -1, 2, 8, 7, 3, 5]

    raw = questionary.text(
        'Введите массив через пробел или запятую:',
        instruction='Например: 1 3 -1 2 8 7 3 5',
        style=custom_style,
    ).ask()

    tokens = raw.replace(',', ' ').split()
    return [int(t) for t in tokens]


# ================== Меню алгоритмов ==================


def run_numeric_algos():
    while True:
        algo_name = questionary.select(
            'Выберите числовой алгоритм:',
            choices=[
                Choice('fib — Fibonacci (итеративно)', 'fib'),
                Choice('fibrec — Fibonacci (рекурсивно)', 'fibrec'),
                Choice('Fib01 — Fibonacci (DP)', 'Fib01'),
                Separator(),
                Choice('factorial — итеративный', 'factorial'),
                Choice('factorialrec — рекурсивный', 'factorialrec'),
                Separator(),
                Choice('⬅ Назад', 'back'),
            ],
            style=custom_style,
        ).ask()

        if algo_name == 'back':
            return

        if algo_name not in ALGO_FUNCS:
            questionary.print(
                f"[!] Алгоритм '{algo_name}' не найден в registry.",
                style='bold fg:ansired',
            )
            continue

        n = ask_int('n = ', min_value=0)
        func = ALGO_FUNCS[algo_name]

        try:
            result = func(n)
            questionary.print(
                f'Результат ({algo_name}) для n={n}: {result}',
                style='bold fg:ansigreen',
            )
        except Exception as e:
            questionary.print(
                f'[X] Ошибка при выполнении {algo_name}: {e}',
                style='bold fg:ansired',
            )


def ask_positive_int(message: str, min_value: int = 1) -> int:
    def _validate(text: str):
        if not text.strip().isdigit():
            return 'Нужно целое число'
        value = int(text)
        if value < min_value:
            return f'Число должно быть ≥ {min_value}'
        return True

    raw = questionary.text(message, validate=_validate, style=custom_style).ask()
    return int(raw)


def ask_optional_positive_int(message: str, min_value: int = 1) -> int | None:
    def _validate(text: str):
        if text.strip() == '':
            return True
        if not text.strip().isdigit():
            return 'Нужно целое число или пустая строка'
        value = int(text)
        if value < min_value:
            return f'Число должно быть ≥ {min_value}'
        return True

    raw = questionary.text(
        message,
        instruction='Enter для значения по умолчанию',
        validate=_validate,
        style=custom_style,
    ).ask()

    if raw.strip() == '':
        return None
    return int(raw)


def ask_array_for_int() -> list[int]:
    arr = ask_array()  # как у тебя сейчас, только возвращает list[int]
    return arr


def ask_array_for_float() -> list[float]:
    use_default = questionary.confirm(
        'Использовать тестовый массив [1.0, 3.2, -1.5, 2.0, 8.1, 7.7, 3.3, 5.0]?',
        default=True,
        style=custom_style,
    ).ask()

    if use_default:
        return [1.0, 3.2, -1.5, 2.0, 8.1, 7.7, 3.3, 5.0]

    raw = questionary.text(
        'Введите массив через пробел или запятую:',
        instruction='Например: 1.0 3.2 -1.5 2 8.1 7.7 3.3 5',
        style=custom_style,
    ).ask()

    tokens = raw.replace(',', ' ').split()
    return [float(t) for t in tokens]


def run_sorts():
    while True:
        sort_name = questionary.select(
            'Выберите алгоритм сортировки:',
            choices=[
                Choice('bubble — пузырьковая', 'bubble'),
                Choice('quick — быстрая', 'quick'),
                Choice('counting — подсчётом', 'counting'),
                Choice('heap — кучей', 'heap'),
                Choice('radix — по разрядам', 'radix'),
                Choice('bucket — блочная', 'bucket'),
                Separator(),
                Choice('⬅ Назад', 'back'),
            ],
            style=custom_style,
        ).ask()

        if sort_name == 'back':
            return

        if sort_name not in SORT_FUNCS:
            questionary.print(
                f"[!] Алгоритм сортировки '{sort_name}' не найден в registry.",
                style='bold fg:ansired',
            )
            continue

        # Ввод массива в зависимости от типа сортировки
        if sort_name == 'bucket':
            arr = ask_array_for_float()
        else:
            arr = ask_array_for_int()

        func = SORT_FUNCS[sort_name]

        # Дополнительные параметры
        kwargs = {}
        if sort_name == 'radix':
            base = ask_positive_int('base = ', min_value=2)
            kwargs['base'] = base
        elif sort_name == 'bucket':
            buckets = ask_optional_positive_int('buckets = ', min_value=1)
            kwargs['buckets'] = buckets

        try:
            sorted_arr = func(arr, **kwargs)
            questionary.print(f'Исходный массив: {arr}', style='bold fg:ansicyan')
            questionary.print(
                f'После {sort_name}_sort (параметры: {kwargs or "по умолчанию"}): {sorted_arr}',
                style='bold fg:ansigreen',
            )
        except NotImplementedError as e:
            questionary.print(f'[~] {e}', style='bold fg:ansiyellow')
        except Exception as e:
            questionary.print(
                f'[X] Ошибка при выполнении {sort_name}: {e}',
                style='bold fg:ansired',
            )


# ================== Главное меню ==================


def main():
    while True:
        choice = questionary.select(
            'Что вы хотите сделать?',
            choices=[
                Choice('Алгоритмы на числах (fib, factorial…)', 'numeric'),
                Choice('Алгоритмы сортировки', 'sorts'),
                Separator(),
                Choice('Выйти', 'exit'),
            ],
            style=custom_style,
        ).ask()

        if choice == 'exit' or choice is None:
            questionary.print('Пока!', style='bold fg:ansigreen')
            break
        elif choice == 'numeric':
            run_numeric_algos()
        elif choice == 'sorts':
            run_sorts()


if __name__ == '__main__':
    main()
