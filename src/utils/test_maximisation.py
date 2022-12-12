import pytest
from .modulo_maximisation import naive, efficient

lists = ([5, 4], [7, 8, 9], [5, 7, 8, 9, 10])
m = 40
f = lambda x: x**2


def test_naive():
    value = naive(lists, m, f)
    assert value == 37


def test_efficient():
    value = efficient(lists, m, f)
    assert value == 37
