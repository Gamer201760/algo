from functools import wraps
from typing import Callable, get_args, get_origin, get_type_hints


class Register:
    def __init__(self) -> None:
        self._funcs: dict[str, Callable] = {}

    def reg(self, func: Callable):
        self._funcs[func.__name__] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    def exec(self, name: str):
        data = ['12', '1 2 4 112 0']
        kwargs = {}
        for n, t in annotations(self._funcs[name]):
            print(n, t, get_origin(t), get_args(t))
            if get_origin(t) is list:
                kwargs[n] = str_to_list(data[1], get_args(t)[0])
            else:
                kwargs[n] = t(data[0])
        self._funcs[name](**kwargs)


def str_to_list[T](data: str, parser: Callable[[str], T]) -> list[T]:
    return [parser(x) for x in data.split()]


def annotations(func: Callable) -> list[tuple[str, type]]:
    type_hints = get_type_hints(func)
    return [(name, t) for name, t in type_hints.items()][:-1]


a = Register()


@a.reg
def bubble(a: list[str], b: int) -> list[int]:
    """Сортировка пузырьком"""
    print('a', a)
    print('b', b, type(b))
    return []


if __name__ == '__main__':
    a.exec('bubble')
