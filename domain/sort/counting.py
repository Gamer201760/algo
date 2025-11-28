from typing import Any, Callable


def counting_sort[T](
    a: list[int],
    *,
    key: Callable[[T], Any] | None = None,
) -> list[int]: ...
