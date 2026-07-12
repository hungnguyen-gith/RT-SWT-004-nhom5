from functions.PY_079 import factorial
import pytest

def test_factorial_normal_cases():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(10) == 3628800

def test_factorial_with_mod():
    assert factorial(5, mod=7) == 1
    assert factorial(5, mod=5) == 0
    assert factorial(10, mod=100) == 80
    assert factorial(10, mod=3628800) == 3628800

def test_factorial_edge_cases():
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24

def test_factorial_invalid_input():
    with pytest.raises(ValueError, match="'n' must be a non-negative integer."):
        factorial(-1)
    with pytest.raises(ValueError, match="'n' must be a non-negative integer."):
        factorial(1.5)
    with pytest.raises(ValueError, match="'mod' must be a positive integer"):
        factorial(5, mod=-1)
    with pytest.raises(ValueError, match="'mod' must be a positive integer"):
        factorial(5, mod=0)
    with pytest.raises(ValueError, match="'mod' must be a positive integer"):
        factorial(5, mod=1.5)