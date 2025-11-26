import inspect
from dataclasses import dataclass
from typing import (
    Annotated,
    Any,
    Iterable,
    List,
    Sequence,
    Type,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

V = TypeVar('V')


@dataclass(frozen=True)
class ParamInfo:
    """
    name: имя параметра
    base_type: тип без Annotated (int, list[int], ...)
    origin: origin из typing.get_origin(base_type) (list, dict, Union, ...)
    args: args из typing.get_args(base_type) (для list[int] -> (int,))
    metadata: список метаданных из Annotated (MinValue, MaxValue, ...)
    param: inspect.Parameter
    """

    name: str
    base_type: Any
    origin: Any | None
    args: tuple[Any, ...]
    metadata: List[Any]
    param: inspect.Parameter


def _split_annotated(annotated_type: Any) -> tuple[Any, List[Any]]:
    """Если тип Annotated[T, meta...], вернуть (T, [meta...]), иначе (тип, [])"""
    if get_origin(annotated_type) is Annotated:
        base_type, *meta = get_args(annotated_type)
        return base_type, list(meta)
    return annotated_type, []


def iter_parameters(func: Any) -> Iterable[ParamInfo]:
    """
    Итератор по параметрам функции с учётом Annotated
    """
    hints = get_type_hints(func, include_extras=True)
    sig = inspect.signature(func)

    for name, param in sig.parameters.items():
        if name not in hints:
            continue

        annotated_type = hints[name]
        base_type, metadata = _split_annotated(annotated_type)

        origin = get_origin(base_type)
        args = get_args(base_type)

        yield ParamInfo(
            name=name,
            base_type=base_type,
            origin=origin,
            args=args,
            metadata=metadata,
            param=param,
        )


def extract_validators(meta: Sequence[Any], validator_cls: Type[V]) -> List[V]:
    return [m for m in meta if isinstance(m, validator_cls)]
