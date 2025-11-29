from typing import Protocol


class StackProtocol(Protocol):
    def push(self, x: int) -> None:
        raise NotImplementedError

    def pop(self) -> int:
        raise NotImplementedError

    def peek(self) -> int:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def min(self) -> int:
        raise NotImplementedError


class MinStack:
    def __init__(self) -> None:
        self._data: list[int] = []
        self._mins: list[int] = []

    def push(self, x: int) -> None:
        self._data.append(x)
        if not self._mins:
            self._mins.append(x)
        else:
            self._mins.append(min(x, self._mins[-1]))

    def pop(self) -> int:
        if not self._data:
            raise IndexError('pop from empty stack')
        self._mins.pop()
        return self._data.pop()

    def peek(self) -> int:
        if not self._data:
            raise IndexError('peek from empty stack')
        return self._data[-1]

    def is_empty(self) -> bool:
        return not self._data

    def __len__(self) -> int:
        return len(self._data)

    def min(self) -> int:
        if not self._mins:
            raise ValueError('min from empty stack')
        return self._mins[-1]

    def list(self) -> list[int]:
        return self._data
