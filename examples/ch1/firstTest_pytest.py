import pytest


def test_sum():
    res = sum([2, 4, 6])
    assert res == 12

def test_sum_fail_str():
    with pytest.raises(TypeError):
        res = sum("SOMESTRING")
