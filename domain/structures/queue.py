from typing import Protocol

from domain.structures.stack import MinStack, StackProtocol


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


class TwoStackQueue(QueueProtocol):
    def __init__(self) -> None:
        self._in: StackProtocol = MinStack()
        self._out: StackProtocol = MinStack()

    def _move_in_to_out(self) -> None:
        if self._out.is_empty():
            while not self._in.is_empty():
                self._out.push(self._in.pop())

    def enqueue(self, x: int) -> None:
        self._in.push(x)

    def dequeue(self) -> int:
        if self.is_empty():
            raise IndexError('dequeue from empty queue')
        self._move_in_to_out()
        return self._out.pop()

    def front(self) -> int:
        if self.is_empty():
            raise IndexError('front from empty queue')
        self._move_in_to_out()
        return self._out.peek()

    def is_empty(self) -> bool:
        return self._in.is_empty() and self._out.is_empty()

    def __len__(self) -> int:
        return len(self._in) + len(self._out)
