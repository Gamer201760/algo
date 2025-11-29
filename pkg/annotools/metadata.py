from typing import Protocol


class MetaData(Protocol): ...


class Message(MetaData):
    def __init__(self, m: str) -> None:
        self._m = m

    def msg(self) -> str:
        return self._m
