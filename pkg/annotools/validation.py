from dataclasses import dataclass


class ValidationError(Exception): ...


class IntValidator:
    def validate(self, value: int) -> None:
        """Выбрасывает ValidationError при ошибке"""
        raise NotImplementedError


@dataclass(frozen=True)
class MinValue(IntValidator):
    limit: int

    def validate(self, value: int) -> None:
        if value < self.limit:
            raise ValidationError(f'Число должно быть >= {self.limit}')


@dataclass(frozen=True)
class MaxValue(IntValidator):
    limit: int

    def validate(self, value: int) -> None:
        if value > self.limit:
            raise ValidationError(f'Число должно быть <= {self.limit}')
