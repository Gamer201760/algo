from typing import Callable

import questionary

from adapter.cli.style import STYLE
from adapter.cli.validator import validator_factory, validator_token_factory
from pkg.annotools.validation import Validator


def ask[T](
    message: str,
    parser: Callable[[str], T],
    *,
    validators: list[Validator] | None = None,
) -> T:
    raw = questionary.text(
        message, validate=validator_factory(validators), style=STYLE
    ).unsafe_ask()
    return parser(raw)


def ask_default[T](default: T, message: str) -> T | None:
    use_default = questionary.confirm(
        message,
        default=True,
        style=STYLE,
    ).unsafe_ask()

    if use_default:
        return default


def ask_array[T](
    parser: Callable[[str], T],
    *,
    validators: list[Validator] | None = None,
) -> list[T]:
    raw = questionary.text(
        'Введите массив через пробел или запятую:',
        instruction='Например: 1 3 -1 2 8 7 3 5',
        style=STYLE,
        validate=validator_token_factory(validators),
    ).unsafe_ask()

    tokens = raw.replace(',', ' ').split()
    return [parser(t) for t in tokens]
