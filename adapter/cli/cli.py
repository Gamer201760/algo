from typing import (
    Annotated,
    Any,
    Callable,
    Dict,
)

import questionary
from questionary import Choice, Separator

from adapter.cli.ask import ask, ask_array
from adapter.cli.style import STYLE
from adapter.cli.validator import ZNumValidator
from domain.structures.stack import MinStack
from pkg.annotools import (
    extract_validators,
    iter_parameters,
)
from pkg.annotools.annotations import extract_annotaded
from pkg.annotools.validation import MinValue, TypeValidator


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
        # list[T]
        if info.base_type is list:
            if len(info.args) != 1:
                raise TypeError('У списка должен ровно один аннотированый тип')
            btype, meta = extract_annotaded(info.args[0])
            kwargs[info.name] = ask_array(btype, validators=extract_validators(meta))
            continue

        if info.base_type not in (int, float, str, bool):
            raise TypeError(f'{info.base_type.__name__} не поддерживается парсером')
        validators = extract_validators(info.metadata)
        kwargs[info.name] = ask(f'{info.name} =', info.base_type, validators=validators)

    return kwargs


@r
def list_test_int(n: list[int]) -> int:
    """Тест листа int"""
    return 10


@r
def list_test_float(n: list[float]):
    """Тест листа float"""
    return n


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
def list_float(n: float):
    """float"""
    return n


@r
def list_dict(n: dict):
    """dict"""
    return n


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
            style=STYLE,
        ).unsafe_ask()
        if choice == 'push':
            s.push(ask('Введите элемент', int))
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
            style=STYLE,
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
        questionary.print('Пока!', style='bold fg:ansigreen')
