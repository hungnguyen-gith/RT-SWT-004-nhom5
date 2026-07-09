import pytest

def test_merge_intervals():
    assert merge_intervals([]) == []
    assert merge_intervals([(1, 3), (2, 4)]) == [(1, 4)]
    assert merge_intervals([(1, 3), (4, 6)]) == [(1, 3), (4, 6)]
    assert merge_intervals([(1, 4), (2, 3)]) == [(1, 4)]
    assert merge_intervals([(1, 2), (3, 4), (5, 6)]) == [(1, 2), (3, 4), (5, 6)]
    assert merge_intervals([(1, 4), (0, 4)]) == [(0, 4)]
    assert merge_intervals([(1, 5), (2, 3), (4, 6)]) == [(1, 6)]
    assert merge_intervals([(1, 10), (2, 3), (4, 5), (6, 7), (8, 9)]) == [(1, 10)]
    assert merge_intervals([(1, 2), (3, 5), (4, 6)]) == [(1, 2), (3, 6)]