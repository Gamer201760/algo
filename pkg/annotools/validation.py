from dataclasses import dataclass
from typing import Callable, Protocol, runtime_checkable

from pkg.annotools.metadata import MetaData


class ValidationError(Exception): ...


@runtime_checkable
class Validator(MetaData, Protocol):
    def validate(self, value: str) -> None:
        """Выбрасывает ValidationError при ошибке"""
        raise NotImplementedError


@dataclass(frozen=True)
class TypeValidator[T]:
    t: Callable[[str], T]

    def validate(self, value: str) -> None:
        try:
            self.t(value)
        except Exception:
            raise ValidationError(
                f'Не удалось {value} привести к типу {self.t.__name__}'
            )


@dataclass(frozen=True)
class StrLen:
    limit: int

    def validate(self, value: str) -> None:
        if len(value) > self.limit:
            raise ValidationError(f'Строка должна быть <= {self.limit}')


@dataclass(frozen=True)
class MinValue:
    limit: int

    def validate(self, value: str) -> None:
        if int(value) < self.limit:
            raise ValidationError(f'Число должно быть >= {self.limit}')


@dataclass(frozen=True)
class MaxValue:
    limit: int

    def validate(self, value: str) -> None:
        if int(value) > self.limit:
            raise ValidationError(f'Число должно быть <= {self.limit}')
