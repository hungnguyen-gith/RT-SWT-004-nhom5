import pytest

from your_module import factorial  # Replace 'your_module' with the actual module name

def test_factorial_normal_cases():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(10) == 3628800

def test_factorial_with_mod():
    assert factorial(5, mod=7) == 1
    assert factorial(10, mod=100) == 80
    assert factorial(6, mod=5) == 0

def test_factorial_boundary_cases():
    assert factorial(2) == 2
    assert factorial(3) == 6
    assert factorial(4) == 24

def test_factorial_edge_cases():
    assert factorial(0, mod=1) == 0
    assert factorial(1, mod=1) == 0
    assert factorial(5, mod=1) == 0

def test_factorial_invalid_inputs():
    with pytest.raises(ValueError):
        factorial(-1)
    with pytest.raises(ValueError):
        factorial(5, mod=-1)
    with pytest.raises(ValueError):
        factorial(5, mod=0)
    with pytest.raises(ValueError):
        factorial(5.5)
    with pytest.raises(ValueError):
        factorial("string")