from typing import Callable

import questionary

from adapter.cli.style import STYLE
from adapter.cli.validator import validator_factory, validator_token_factory
from pkg.annotools.validation import Validator


def ask_int(
    message: str,
    *,
    validators: list[Validator] | None = None,
) -> int:
    raw = questionary.text(
        message, validate=validator_factory(validators), style=STYLE
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
        style=STYLE,
    ).ask()

    if use_default:
        sample = [1, 3, -1, 2, -8, 7, 3, 5]
        return [parser(str(x)) for x in sample]

    raw = questionary.text(
        'Введите массив через пробел или запятую:',
        instruction='Например: 1 3 -1 2 8 7 3 5',
        style=STYLE,
        validate=validator_token_factory(validators),
    ).ask()

    tokens = raw.split(', ')
    return [parser(t) for t in tokens]
