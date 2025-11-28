from typing import Any, Callable


def bucket_sort[T](
    a: list[int],
    *,
    buckets: int | None = None,
    key: Callable[[T], Any] | None = None,
) -> list[int]: ...
