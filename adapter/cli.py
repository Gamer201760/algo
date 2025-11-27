from typing import (
    Annotated,
    Any,
    Callable,
    Dict,
)

import questionary
from questionary import Choice, Separator, Style

from domain.structures.stack import MinStack
from pkg.annotools import (
    ValidationError,
    extract_validators,
    iter_parameters,
)
from pkg.annotools.annotations import extract_annotaded
from pkg.annotools.validation import MinValue, TypeValidator, Validator


class Register:
    """Простой реестр функций по имени"""

    def __init__(self) -> None:
        self._funcs: Dict[str, Callable] = {}

    def __call__(self, func: Callable) -> Callable:
        self._funcs[func.__name__] = func
        return func

    @property
    def funcs(self) -> Dict[str, Callable]:
        return self._funcs.copy()


r = Register()


def build_kwargs(func: Callable[..., Any]) -> dict[str, Any]:
    kwargs: dict[str, Any] = {}

    for info in iter_parameters(func):
        print(info)
        # scalar int
        if info.base_type is int:
            validators = extract_validators(info.metadata)
            kwargs[info.name] = ask_int(f'{info.name} =', validators=validators)
            continue

        # list[T]
        if info.base_type is list:
            if len(info.args) != 1:
                raise TypeError('У списка должен ровно один аннотированый тип')
            btype, meta = extract_annotaded(info.args[0])
            kwargs[info.name] = ask_array(btype, validators=extract_validators(meta))
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


def validator_token_factory(validators: list[Validator] | None = None):
    validators = validators or []

    def _validate(
        text: str,
    ) -> str | bool:
        token = text.split(', ')[-1]
        for v in validators:
            try:
                v.validate(token)
            except ValidationError as e:
                return str(e)
        return True

    return _validate


def validator_factory(validators: list[Validator] | None = None):
    validators = validators or []

    def _validate(
        text: str,
    ) -> str | bool:
        for v in validators:
            try:
                v.validate(text)
            except ValidationError as e:
                return str(e)
        return True

    return _validate


class ZNumValidator:
    def validate(self, value: str) -> None:
        if not value or not value.lstrip('-').isdigit():
            raise ValidationError('Нужно целое число')


def ask_int(
    message: str,
    *,
    validators: list[Validator] | None = None,
) -> int:
    raw = questionary.text(
        message, validate=validator_factory(validators), style=custom_style
    ).ask()
    return int(raw)


def ask_array[T](
    parser: Callable[[str], T],
    *,
    validators: list[Validator] | None = None,
) -> list[T]:
    use_default = questionary.confirm(
        'Использовать тестовый массив [1, 3, -1, 2, -8, 7, 3, 5]?',
        default=True,
        style=custom_style,
    ).ask()

    if use_default:
        sample = [1, 3, -1, 2, -8, 7, 3, 5]
        return [parser(str(x)) for x in sample]

    raw = questionary.text(
        'Введите массив через пробел или запятую:',
        instruction='Например: 1 3 -1 2 8 7 3 5',
        style=custom_style,
        validate=validator_token_factory(validators),
    ).ask()

    tokens = raw.split(', ')
    return [parser(t) for t in tokens]


# ---------------- Алгоритмы ----------------


@r
def list_test_int(n: list[int]) -> int:
    """Тест листа int"""
    return 10


@r
def list_test_empty(n: list) -> int:
    """Тест листа empty"""
    return 10


@r
def list_test_str(n: list[str]) -> int:
    """Тест листа str"""
    print(n)
    return 10


@r
def list_str(n: str) -> int:
    """str"""
    return 10


@r
def list_int(n: int) -> int:
    """int"""
    return 10


@r
def list_int_anno(
    n: list[Annotated[int, ZNumValidator(), TypeValidator(int), MinValue(10)]],
) -> list:
    """anno int"""
    return n


@r
def list_float(n: float) -> int:
    """float"""
    return 10


@r
def stack():
    """Стэк"""
    s = MinStack()
    while True:
        choice = questionary.select(
            'Выберите',
            choices=[
                Choice('Push', 'push'),
                Choice('Pop', 'pop'),
                Choice('Peek', 'peek'),
                Choice('Min', 'min'),
                Separator(),
                Choice('Назад', 'back'),
            ],
            style=custom_style,
        ).ask()
        if choice == 'push':
            s.push(ask_int('Введите элемент'))
        elif choice == 'pop':
            questionary.print(str(s.pop()))
        elif choice == 'peek':
            questionary.print(str(s.peek()))
        elif choice == 'min':
            questionary.print(str(s.min()))

        questionary.print(
            '[' + ', '.join(map(str, s.list())) + '], MIN: ' + str(s.min())
        )
        if choice in ('back', None):
            break


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
            break

        func = r.funcs[choice]
        kwargs = build_kwargs(func)
        try:
            result = func(**kwargs)
            if result:
                questionary.print(f'Результат: {result}', style='bold fg:ansiyellow')
        except (ValueError, IndexError) as e:
            questionary.print('Error: ' + str(e), style='bold fg:red')

    questionary.print('Пока!', style='bold fg:ansigreen')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        ...
