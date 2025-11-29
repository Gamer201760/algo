from typing import (
    Annotated,
)

import questionary
from questionary import Choice, Separator

from adapter.cli.ask import ask
from adapter.cli.cli import CLI
from adapter.cli.style import STYLE
from adapter.cli.validator import ZNumValidator
from domain.algo.factorial import factorial, factorial_recursive
from domain.algo.fib import fibo, fibo_recursive
from domain.structures.stack import MinStack
from pkg.annotools.validation import MaxValue, MinValue, TypeValidator

cli = CLI()


@cli
def fibonacci_iter(
    n: Annotated[
        int, ZNumValidator(), TypeValidator(int), MinValue(0), MaxValue(20577)
    ],
) -> int:
    """Фибоначчи итерируемая"""
    return fibo(n)


@cli
def fibonacci_rec(
    n: Annotated[int, ZNumValidator(), TypeValidator(int), MinValue(0), MaxValue(30)],
) -> int:
    """Фибоначчи рекурсивная"""
    return fibo_recursive(n)


@cli
def factorial_iter(
    n: Annotated[
        int,
        ZNumValidator(),
        TypeValidator(int),
        MinValue(0),
        MaxValue(1558),
    ],
) -> int:
    """Факториал итерируемый"""
    return factorial(n)


@cli
def factorial_rec(
    n: Annotated[
        int,
        ZNumValidator(),
        TypeValidator(int),
        MinValue(0),
        MaxValue(996),
    ],
) -> int:
    """Факториал рекурсивный"""
    return factorial_recursive(n)


@cli
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
