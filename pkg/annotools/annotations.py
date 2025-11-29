import inspect
from dataclasses import dataclass
from typing import (
    Annotated,
    Any,
    Iterable,
    Sequence,
    get_args,
    get_origin,
    get_type_hints,
)

from pkg.annotools.metadata import Message, MetaData
from pkg.annotools.validation import Validator


@dataclass(frozen=True)
class ParamInfo:
    name: str
    base_type: Any  # int, str, float, MyClass, ...
    args: tuple[Any, ...]  # параметры generic (для list[int] -> (int,))
    metadata: list[MetaData]
    default: Any = None


def _split_annotated(annotated_type: Any) -> tuple[Any, list[Any]]:
    """Если тип Annotated[T, meta...], вернуть (T, [meta...]), иначе (тип, [])"""
    if get_origin(annotated_type) is Annotated:
        base_type, *meta = get_args(annotated_type)
        return base_type, list(meta)
    return annotated_type, []


def extract_annotaded(t: Any) -> tuple[Any, list]:
    base_type, metadata = _split_annotated(t)

    origin = get_origin(base_type)
    if origin is not None:
        base_type = origin
    return (
        base_type,
        metadata,
    )


def iter_parameters(func: Any) -> Iterable[ParamInfo]:
    """
    Итератор по параметрам функции с учётом Annotated.
    base_type/args уже нормализованы (origin + args)
    """
    hints = get_type_hints(func, include_extras=True)
    sig = inspect.signature(func)

    for name, param in sig.parameters.items():
        if name not in hints:
            continue

        base_type, metadata = _split_annotated(hints[name])

        origin = get_origin(base_type)
        args = get_args(base_type)
        if origin is not None:
            base_type = origin

        default = None
        if param.default is not inspect._empty:
            default = param.default

        yield ParamInfo(
            name=name,
            base_type=base_type,
            args=args,
            metadata=metadata,
            default=default,
        )


def extract_validators(meta: Sequence[MetaData]) -> list[Validator]:
    return [m for m in meta if isinstance(m, Validator)]


def extract_messages(meta: Sequence[MetaData]) -> list[Message]:
    return [m for m in meta if isinstance(m, Message)]
