from typing import Protocol


class SortingAlgorithm(Protocol):
    @property
    def name(self) -> str: ...
    def sort(self, a: list[int]) -> list[int]: ...
