from functions.PY_073 import trim_front

def test_trim_front_normal_cases():
    assert trim_front(['  0.5', '  1.0', '  2.3']) == ['0.5', '1.0', '2.3']
    assert trim_front(['  0.0', '  0.0', '  0.0']) == ['0.0', '0.0', '0.0']
    assert trim_front(['  1', '  2', '  3']) == ['1', '2', '3']
    assert trim_front(['  0.1', '  0.2', '  0.3']) == ['0.1', '0.2', '0.3']

def test_trim_front_edge_cases():
    assert trim_front(['', '  ', '   ']) == ['', '  ', '   ']
    assert trim_front(['0.0', '0.0', '0.0']) == ['0.0', '0.0', '0.0']
    assert trim_front(['  0', '  1', '  2']) == ['0', '1', '2']
    assert trim_front(['  ', ' 0', ' 1']) == [' ', '0', '1']

def test_trim_front_invalid_input():
    assert trim_front([]) == []
    assert trim_front(['']) == ['']
    assert trim_front(['   1.5', '   2.5']) == ['1.5', '2.5']
    assert trim_front(['   0.0', '   0.0', '   0.0']) == ['0.0', '0.0', '0.0']