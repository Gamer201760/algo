from pkg.annotools.validation import ValidationError, Validator


class ZNumValidator:
    def validate(self, value: str) -> None:
        if not value or not value.lstrip('-').isdigit():
            raise ValidationError('Нужно целое число')


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
