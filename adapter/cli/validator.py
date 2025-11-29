from dataclasses import dataclass

from pkg.annotools.validation import ValidationError, Validator


@dataclass(frozen=True)
class MinValueFloat:
    limit: float

    def validate(self, value: str) -> None:
        if float(value) < self.limit:
            raise ValidationError(f'Число должно быть >= {self.limit}')


@dataclass(frozen=True)
class MaxValueFloat:
    limit: float

    def validate(self, value: str) -> None:
        if float(value) > self.limit:
            raise ValidationError(f'Число должно быть <= {self.limit}')


class NumValidator:
    def validate(self, value: str) -> None:
        if not value or not value.lstrip('-').isdigit():
            raise ValidationError('Нужно целое число')


def validator_token_factory(validators: list[Validator] | None = None):
    validators = validators or []

    def _validate(
        text: str,
    ) -> str | bool:
        token = text.replace(',', ' ').split()
        if len(token) == 0:
            return True
        for v in validators:
            try:
                v.validate(token[-1])
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
