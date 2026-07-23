import pytest

def trim_front(strings):
    trimmed = strings
    while len(strings) > 0 and all(x[0] == ' ' for x in trimmed):
        trimmed = [x[1:] for x in trimmed]
    return trimmed

def test_trim_front_normal_cases():
    assert trim_front(['  hello', '  world']) == ['hello', 'world']
    assert trim_front(['   test', '   case']) == ['test', 'case']
    assert trim_front(['   leading spaces', '   another one']) == ['leading spaces', 'another one']
    assert trim_front(['no spaces', 'here']) == ['no spaces', 'here']

def test_trim_front_boundary_cases():
    assert trim_front(['   ']) == ['']
    assert trim_front(['']) == ['']
    assert trim_front(['   ', '   ']) == ['', '']
    assert trim_front(['  a', '  b', '  c']) == ['a', 'b', 'c']

def test_trim_front_edge_cases():
    assert trim_front([]) == []
    assert trim_front(['']) == ['']
    assert trim_front(['   ', '']) == ['', '']
    assert trim_front(['  single space']) == ['single space']
    assert trim_front(['  ', '  ', '  ']) == ['', '', '']