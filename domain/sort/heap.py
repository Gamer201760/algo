from typing import Any, Callable


def heap_sort[T](
    a: list[int],
    *,
    key: Callable[[T], Any] | None = None,
    cmp: Callable[[T, T], int] | None = None,
) -> list[int]: ...
