from typing import Any, Callable

import questionary
from questionary import Choice, Separator

from adapter.cli.ask import ask, ask_array, ask_default
from adapter.cli.style import STYLE
from pkg.annotools import extract_annotaded, extract_validators, iter_parameters
from pkg.annotools.annotations import extract_messages


class CLI:
    def __init__(self, style=STYLE) -> None:
        self._handlers: dict[str, Callable[..., Any]] = {}
        self._style = style

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """Регистрирует функцию как хендлер по её имени"""
        self._handlers[func.__name__] = func
        return func

    @property
    def handlers(self) -> dict[str, Callable[..., Any]]:
        return self._handlers.copy()

    def _build_kwargs(self, func: Callable[..., Any]) -> dict[str, Any]:
        """Сбор kwargs на основе аннотаций и метаданных Annotated"""
        kwargs: dict[str, Any] = {}

        for info in iter_parameters(func):
            for msg in extract_messages(info.metadata):
                questionary.print(msg.msg(), style='bold fg:ansigreen')

            if info.default is not None:
                default = ask_default(
                    info.default, f'Использовать {info.name} = {info.default}?'
                )
                if default is not None:
                    kwargs[info.name] = default
                    continue
            # list[T]
            if info.base_type is list:
                if len(info.args) != 1:
                    raise TypeError('У списка должен ровно один аннотированный тип')
                btype, meta = extract_annotaded(info.args[0])
                kwargs[info.name] = ask_array(
                    btype,
                    validators=extract_validators(meta),
                )
                continue

            if info.base_type not in (int, float, str, bool):
                raise TypeError(f'{info.base_type.__name__} не поддерживается парсером')

            validators = extract_validators(info.metadata)
            kwargs[info.name] = ask(
                f'{info.name} =',
                info.base_type,
                validators=validators,
            )

        return kwargs

    def run(self) -> None:
        try:
            while True:
                choice = questionary.select(
                    'Выберите',
                    choices=[
                        *(
                            Choice(func.__doc__ or name, name)
                            for name, func in self._handlers.items()
                        ),
                        Separator(),
                        Choice('Выйти', 'exit'),
                    ],
                    style=self._style,
                ).ask()

                if choice in ('exit', None):
                    break

                func = self._handlers[choice]
                kwargs = self._build_kwargs(func)
                try:
                    result = func(**kwargs)
                    if result:
                        questionary.print(
                            f'Результат: {result}',
                            style='bold fg:ansiyellow',
                        )
                except (ValueError, IndexError) as e:
                    questionary.print('Error: ' + str(e), style='bold fg:red')
        except KeyboardInterrupt:
            pass
        questionary.print('Пока!', style='bold fg:ansigreen')
