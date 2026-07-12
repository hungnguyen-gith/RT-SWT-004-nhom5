from functions.PY_080 import three_sum

def test_three_sum_normal_cases():
    assert three_sum([-1, 0, 1, 2, -1, -4]) == {(-1, -1, 2), (-1, 0, 1)}
    assert three_sum([0, 0, 0]) == {(0, 0, 0)}
    assert three_sum([1, 2, -2, -1]) == set()
    assert three_sum([-2, 0, 1, 1, 2]) == {(-2, 1, 1)}

def test_three_sum_edge_cases():
    assert three_sum([]) == set()
    assert three_sum([1]) == set()
    assert three_sum([1, 2]) == set()
    assert three_sum([0, 0, 0, 0]) == {(0, 0, 0)}

def test_three_sum_invalid_input():
    import pytest
    with pytest.raises(TypeError):
        three_sum(None)
    with pytest.raises(TypeError):
        three_sum("string")
    with pytest.raises(TypeError):
        three_sum(123)
    with pytest.raises(TypeError):
        three_sum([1, 2, "three"])