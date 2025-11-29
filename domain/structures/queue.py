from typing import Protocol


class QueueProtocol(Protocol):
    def enqueue(self, x: int) -> None:
        raise NotImplementedError

    def dequeue(self) -> int:
        raise NotImplementedError

    def front(self) -> int:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError
