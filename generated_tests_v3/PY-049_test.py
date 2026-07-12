from functions.PY_049 import merge_intervals
import pytest

def test_merge_intervals_normal_cases():
    assert merge_intervals([(1, 3), (2, 4), (5, 7), (6, 8)]) == [(1, 4), (5, 8)]
    assert merge_intervals([(1, 4), (2, 3)]) == [(1, 4)]
    assert merge_intervals([(1, 2), (3, 4), (5, 6)]) == [(1, 2), (3, 4), (5, 6)]
    assert merge_intervals([(1, 5), (2, 3), (4, 6)]) == [(1, 6)]
    assert merge_intervals([(1, 10), (2, 6), (8, 10), (15, 18), (17, 20)]) == [(1, 10), (15, 20)]

def test_merge_intervals_edge_cases():
    assert merge_intervals([]) == []
    assert merge_intervals([(1, 1)]) == [(1, 1)]
    assert merge_intervals([(1, 5), (5, 10)]) == [(1, 10)]
    assert merge_intervals([(1, 3), (3, 5), (5, 7)]) == [(1, 7)]
    assert merge_intervals([(1, 2), (2, 3), (3, 4), (4, 5)]) == [(1, 5)]

def test_merge_intervals_invalid_input():
    with pytest.raises(TypeError):
        merge_intervals(None)
    with pytest.raises(TypeError):
        merge_intervals("not a list")
    with pytest.raises(TypeError):
        merge_intervals([(1, 2), (3, "four")])
    with pytest.raises(TypeError):
        merge_intervals([(1, 2), (3, None)])
    with pytest.raises(TypeError):
        merge_intervals([(1, 2), (3, 4, 5)])  # Invalid tuple length
    with pytest.raises(TypeError):
        merge_intervals([(1, 2), (3,)])  # Invalid tuple length
    with pytest.raises(TypeError):
        merge_intervals([(1, 2), (3, 4)])  # Valid input to ensure no TypeError