from typing import Callable, Dict


class Register:
    """Простой реестр функций по имени."""

    def __init__(self) -> None:
        self._funcs: Dict[str, Callable] = {}

    def __call__(self, func: Callable) -> Callable:
        self._funcs[func.__name__] = func
        return func

    @property
    def funcs(self) -> Dict[str, Callable]:
        return self._funcs.copy()
