from typing import (
    Annotated,
    Any,
    Callable,
    TypeVar,
)

import questionary
from questionary import Choice, Separator, Style

from pkg.annotools import (
    IntValidator,
    MinValue,
    Register,
    ValidationError,
    extract_validators,
    iter_parameters,
)

T = TypeVar('T')

r = Register()


def build_kwargs_for(func: Callable[..., Any]) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}

    for info in iter_parameters(func):
        # scalar int
        if info.origin is None and info.base_type is int:
            validators = extract_validators(info.metadata, IntValidator)
            kwargs[info.name] = ask_int(f'{info.name} =', validators=validators)
            continue

        # list[int]
        if info.origin is list and len(info.args) == 1 and info.args[0] is int:
            # здесь можно при желании тоже дергать extract_validators и
            # применять валидаторы к каждому элементу списка
            kwargs[info.name] = ask_array(int)
            continue

        # фоллбек
        kwargs[info.name] = questionary.text(f'{info.name} =', style=custom_style).ask()

    return kwargs


# ---------------- Стиль questionary ----------------


custom_style = Style(
    [
        ('qmark', 'fg:#00ff7f bold'),
        ('question', 'bold'),
        ('answer', 'fg:#ffb86c bold'),
        ('pointer', 'fg:#00ff7f bold'),
        ('highlighted', 'fg:#00ff7f bold'),
        ('selected', 'fg:#00ff7f bold'),
        ('separator', 'fg:#444444'),
        ('instruction', 'fg:#888888'),
    ]
)


# ---------------- Вопросы ----------------


def ask_int(
    message: str,
    *,
    validators: list[IntValidator] | None = None,
) -> int:
    validators = validators or []

    def _validate(text: str) -> bool | str:
        text = text.strip()
        if not text or not text.lstrip('-').isdigit():
            return 'Нужно целое число'

        value = int(text)

        for v in validators:
            try:
                v.validate(value)
            except ValidationError as e:
                return str(e)

        return True

    raw = questionary.text(message, validate=_validate, style=custom_style).ask()
    return int(raw)


def ask_array(parser: Callable[[str], T], *, default_sample: bool = True) -> list[T]:
    use_default = questionary.confirm(
        'Использовать тестовый массив [1, 3, -1, 2, -8, 7, 3, 5]?',
        default=default_sample,
        style=custom_style,
    ).ask()

    if use_default:
        sample = [1, 3, -1, 2, -8, 7, 3, 5]
        return [parser(str(x)) for x in sample]

    raw = questionary.text(
        'Введите массив через пробел или запятую:',
        instruction='Например: 1 3 -1 2 8 7 3 5',
        style=custom_style,
    ).ask()

    tokens = raw.replace(',', ' ').split()
    return [parser(t) for t in tokens]


# ---------------- Алгоритмы ----------------


@r
def fib(n: Annotated[int, MinValue(0)]) -> int:
    """Итеративный Fibonacci."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@r
def fibrec(n: Annotated[int, MinValue(0)]) -> int:
    """Рекурсивный Fibonacci."""
    if n <= 1:
        return n
    return fibrec(n - 1) + fibrec(n - 2)


@r
def factorial(n: Annotated[int, MinValue(0)]) -> int:
    """Итеративный факториал."""
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res


@r
def factorialrec(n: Annotated[int, MinValue(0)]) -> int:
    """Рекурсивный факториал."""
    if n <= 1:
        return 1
    return n * factorialrec(n - 1)


# ---------------- CLI ----------------


def main() -> None:
    while True:
        choice = questionary.select(
            'Выберите',
            choices=[
                *(Choice(func.__doc__ or name, name) for name, func in r.funcs.items()),
                Separator(),
                Choice('Выйти', 'exit'),
            ],
            style=custom_style,
        ).ask()

        if choice in ('exit', None):
            questionary.print('Пока!', style='bold fg:ansigreen')
            break

        func = r.funcs[choice]
        kwargs = build_kwargs_for(func)
        result = func(**kwargs)
        questionary.print(f'Результат: {result}', style='bold fg:ansiyellow')


if __name__ == '__main__':
    main()
