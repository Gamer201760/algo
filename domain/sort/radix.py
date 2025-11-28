from typing import Any, Callable


def radix_sort[T](
    a: list[int],
    *,
    base: int = 10,
    key: Callable[[T], Any] | None = None,
) -> list[int]: ...
