import pytest

from domain.structures.stack import MinStack


def make_stack() -> MinStack:
    return MinStack()


def test_empty_stack_initial_state():
    s = make_stack()
    assert s.is_empty()
    assert len(s) == 0


def test_push_and_len():
    s = make_stack()
    s.push(10)
    assert not s.is_empty()
    assert len(s) == 1

    s.push(20)
    assert len(s) == 2


def test_lifo_order():
    s = make_stack()
    values = [1, 2, 3, 4, 5]
    for x in values:
        s.push(x)

    result = [s.pop() for _ in range(len(values))]
    assert result == list(reversed(values))
    assert s.is_empty()
    assert len(s) == 0


def test_peek_does_not_remove():
    s = make_stack()
    s.push(1)
    s.push(2)

    assert s.peek() == 2
    assert s.peek() == 2
    assert len(s) == 2

    assert s.pop() == 2
    assert s.peek() == 1
    assert len(s) == 1


def test_pop_from_empty_raises():
    s = make_stack()
    with pytest.raises(IndexError):
        s.pop()


def test_peek_from_empty_raises():
    s = make_stack()
    with pytest.raises(IndexError):
        s.peek()


def test_stack_works_after_being_emptied():
    s = make_stack()
    for x in [1, 2, 3]:
        s.push(x)
    for _ in range(3):
        s.pop()

    assert s.is_empty()
    assert len(s) == 0

    s.push(4)
    s.push(5)
    assert s.pop() == 5
    assert s.pop() == 4
    assert s.is_empty()
