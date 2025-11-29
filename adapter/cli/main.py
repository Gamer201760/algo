from typing import (
    Annotated,
)

import questionary
from questionary import Choice, Separator

from adapter.cli.ask import ask
from adapter.cli.cli import CLI
from adapter.cli.style import STYLE
from adapter.cli.validator import MaxValueFloat, MinValueFloat, NumValidator
from domain.algo.factorial import factorial, factorial_recursive
from domain.algo.fib import fibo, fibo_recursive
from domain.sort import (
    bubble_sort,
    bucket_sort,
    counting_sort,
    heap_sort,
    quick_sort,
    radix_sort,
)
from domain.structures.queue import TwoStackQueue
from domain.structures.stack import MinStack
from pkg.annotools.metadata import Message
from pkg.annotools.validation import MaxValue, MinValue, TypeValidator

cli = CLI()


@cli
def fibonacci_iter(
    n: Annotated[int, NumValidator(), TypeValidator(int), MinValue(0), MaxValue(20577)],
) -> int:
    """Фибоначчи итерируемая"""
    return fibo(n)


@cli
def fibonacci_rec(
    n: Annotated[int, NumValidator(), TypeValidator(int), MinValue(0), MaxValue(30)],
) -> int:
    """Фибоначчи рекурсивная"""
    return fibo_recursive(n)


@cli
def factorial_iter(
    n: Annotated[
        int,
        NumValidator(),
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
        NumValidator(),
        TypeValidator(int),
        MinValue(0),
        MaxValue(996),
    ],
) -> int:
    """Факториал рекурсивный"""
    return factorial_recursive(n)


@cli
def quick(
    a: list[
        Annotated[
            int,
            NumValidator(),
            TypeValidator(int),
        ]
    ] = [1, 3, -1, 2, -8, 7, -3, 5],
):
    """Быстрая сортировка"""
    return quick_sort(a)


@cli
def bubble(
    a: list[
        Annotated[
            int,
            NumValidator(),
            TypeValidator(int),
        ]
    ] = [1, 3, -1, 2, -8, 7, -3, 5],
):
    """Сортировка пузырьком"""
    return bubble_sort(a)


@cli
def radix(
    a: list[
        Annotated[
            int,
            NumValidator(),
            TypeValidator(int),
            MinValue(0),
        ]
    ] = [1, 3, 1, 2, 8, 7, 3, 5],
    base: Annotated[int, NumValidator(), TypeValidator(int), MinValue(1)] = 10,
):
    """Поразрядная сортировка"""
    return radix_sort(a, base=base)


@cli
def counting(
    a: list[
        Annotated[
            int,
            NumValidator(),
            TypeValidator(int),
        ]
    ] = [1, 3, -1, 2, -8, 7, -3, 5],
):
    """Сортировка подсчётом"""
    return counting_sort(a)


@cli
def bucket(
    a: list[
        Annotated[
            float,
            TypeValidator(float),
            MaxValueFloat(1),
            MinValueFloat(0),
        ]
    ] = [0.1, 0.3, 0.1, 0.321432, 0.231, 0.7, 0.12313, 0.2342],
    buckets: Annotated[
        int,
        Message('buckets = -1 значит будет n бакетов'),
        TypeValidator(int),
        MinValue(1),
    ] = -1,
):
    """Карманная сортировка"""
    return bucket_sort(a, buckets=buckets if buckets != -1 else None)


@cli
def heap(
    a: list[
        Annotated[
            int,
            NumValidator(),
            TypeValidator(int),
        ]
    ] = [1, 3, -1, 2, -8, 7, -3, 5],
):
    """Сортировка кучей"""
    return heap_sort(a)


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

        try:
            questionary.print(
                '[' + ', '.join(map(str, s.list())) + '], MIN: ' + str(s.min())
            )
        except ValueError:
            ...

        if choice in ('back', None):
            break


@cli
def queue():
    """Очередь"""
    q = TwoStackQueue()

    while True:
        choice = questionary.select(
            'Выберите',
            choices=[
                Choice('Enqueue', 'enqueue'),
                Choice('Dequeue', 'dequeue'),
                Choice('Front', 'front'),
                Separator(),
                Choice('Назад', 'back'),
            ],
            style=STYLE,
        ).unsafe_ask()

        if choice == 'enqueue':
            q.enqueue(ask('Введите элемент', int))
        elif choice == 'dequeue':
            questionary.print(str(q.dequeue()))
        elif choice == 'front':
            questionary.print(str(q.front()))

        front_repr = 'Нет элментов' if q.is_empty() else str(q.front())
        questionary.print(f'len={len(q)}, empty={q.is_empty()}, front={front_repr}')

        if choice in ('back', None):
            break
