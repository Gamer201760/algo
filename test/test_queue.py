import pytest

from domain.structures.queue import TwoStackQueue


def make_queue() -> TwoStackQueue:
    return TwoStackQueue()


def test_empty_queue_initial_state():
    q = make_queue()
    assert q.is_empty()
    assert len(q) == 0


def test_enqueue_then_len_and_front():
    q = make_queue()
    q.enqueue(10)
    assert not q.is_empty()
    assert len(q) == 1
    assert q.front() == 10

    q.enqueue(20)
    assert len(q) == 2
    assert q.front() == 10  # front не снимает элемент


def test_fifo_order():
    q = make_queue()
    values = [1, 2, 3, 4, 5]
    for x in values:
        q.enqueue(x)

    result = [q.dequeue() for _ in range(len(values))]
    assert result == values
    assert q.is_empty()
    assert len(q) == 0


def test_interleaved_enqueue_dequeue():
    q = make_queue()

    q.enqueue(1)
    q.enqueue(2)
    assert q.dequeue() == 1

    q.enqueue(3)
    assert q.dequeue() == 2
    assert q.front() == 3

    q.enqueue(4)
    assert q.dequeue() == 3
    assert q.dequeue() == 4
    assert q.is_empty()


def test_front_does_not_remove():
    q = make_queue()
    q.enqueue(1)
    q.enqueue(2)

    assert q.front() == 1
    assert q.front() == 1
    assert len(q) == 2

    assert q.dequeue() == 1
    assert q.front() == 2
    assert len(q) == 1


def test_dequeue_from_empty_raises():
    q = make_queue()
    with pytest.raises(IndexError):
        q.dequeue()


def test_front_from_empty_raises():
    q = make_queue()
    with pytest.raises(IndexError):
        q.front()


def test_queue_works_after_being_emptied():
    q = make_queue()
    for x in [1, 2, 3]:
        q.enqueue(x)
    for _ in range(3):
        q.dequeue()

    assert q.is_empty()
    assert len(q) == 0

    q.enqueue(4)
    q.enqueue(5)
    assert q.dequeue() == 4
    assert q.dequeue() == 5
    assert q.is_empty()
