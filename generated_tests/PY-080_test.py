import pytest

def three_sum(array):
    res = set()
    array.sort()
    for i in range(len(array) - 2):
        if i > 0 and array[i] == array[i - 1]:
            continue
        l, r = i + 1, len(array) - 1
        while l < r:
            s = array[i] + array[l] + array[r]
            if s > 0:
                r -= 1
            elif s < 0:
                l += 1
            else:
                res.add((array[i], array[l], array[r]))
                while l < r and array[l] == array[l + 1]:
                    l += 1
                while l < r and array[r] == array[r - 1]:
                    r -= 1
                l += 1
                r -= 1
    return res

def test_three_sum_normal_cases():
    assert three_sum([-1, 0, 1, 2, -1, -4]) == {(-1, -1, 2), (-1, 0, 1)}
    assert three_sum([0, 0, 0]) == {(0, 0, 0)}
    assert three_sum([1, 2, -2, -1]) == set()

def test_three_sum_boundary_cases():
    assert three_sum([]) == set()
    assert three_sum([1]) == set()
    assert three_sum([1, 2]) == set()
    assert three_sum([0, 0, 0, 0]) == {(0, 0, 0)}

def test_three_sum_edge_cases():
    assert three_sum([-1, 0, 1]) == {(-1, 0, 1)}
    assert three_sum([-1, -1, 2, 2, 0]) == {(-1, 0, 1), (-1, -1, 2)}
    assert three_sum([3, -2, 1, 0, -1]) == {(-2, 1, 1), (-1, 0, 1)}
    assert three_sum([-2, 0, 1, 1, 2]) == {(-2, 1, 1)}