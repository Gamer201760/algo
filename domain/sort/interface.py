from typing import Protocol


class SortingAlgorithm(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    def sort(self, a: list[int]) -> list[int]:
        raise NotImplementedError
