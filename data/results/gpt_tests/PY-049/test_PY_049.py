import pytest

def merge_intervals(intervals):
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            if current[1] > last[1]:
                merged[-1] = (last[0], current[1])
        else:
            merged.append(current)
    return merged

def test_merge_intervals():
    # Normal test cases
    assert merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)]) == [(1, 6), (8, 10), (15, 18)]
    assert merge_intervals([(1, 4), (4, 5)]) == [(1, 5)]
    assert merge_intervals([(1, 2), (3, 4), (5, 6)]) == [(1, 2), (3, 4), (5, 6)]
    
    # Boundary test cases
    assert merge_intervals([]) == []
    assert merge_intervals([(1, 1)]) == [(1, 1)]
    assert merge_intervals([(1, 2), (2, 3)]) == [(1, 3)]
    
    # Edge cases
    assert merge_intervals([(1, 5), (2, 3), (4, 6)]) == [(1, 6)]
    assert merge_intervals([(1, 10), (2, 3), (4, 5), (6, 7), (8, 9)]) == [(1, 10)]
    assert merge_intervals([(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]) == [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
    assert merge_intervals([(1, 3), (2, 4), (5, 7), (6, 8), (9, 10)]) == [(1, 4), (5, 8), (9, 10)]