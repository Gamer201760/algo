from typing import Any, Callable


def quick_sort[T](
    a: list[T],
    *,
    key: Callable[[T], Any] | None = None,
    cmp: Callable[[T, T], int] | None = None,
) -> list[T]: ...
