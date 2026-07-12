from functions.PY_067 import akima_interpolate
import numpy as np
import pytest

def test_akima_interpolate_basic():
    xi = np.array([1, 2, 3, 4])
    yi = np.array([1, 4, 9, 16])
    x = np.array([1.5, 2.5, 3.5])
    expected = np.array([2.5, 6.5, 12.5])
    result = akima_interpolate(xi, yi, x)
    np.testing.assert_allclose(result, expected)

def test_akima_interpolate_single_value():
    xi = np.array([1, 2, 3])
    yi = np.array([1, 2, 3])
    x = 2.5
    expected = 2.5
    result = akima_interpolate(xi, yi, x)
    assert result == expected

def test_akima_interpolate_derivative():
    xi = np.array([1, 2, 3, 4])
    yi = np.array([1, 4, 9, 16])
    x = np.array([1.5, 2.5, 3.5])
    der = 1
    expected_derivative = np.array([3, 5, 7])  # Example expected values
    result = akima_interpolate(xi, yi, x, der)
    np.testing.assert_allclose(result, expected_derivative)

def test_akima_interpolate_multiple_derivatives():
    xi = np.array([1, 2, 3, 4])
    yi = np.array([1, 4, 9, 16])
    x = np.array([1.5, 2.5, 3.5])
    der = [0, 1]
    expected_values = [np.array([2.5, 6.5, 12.5]), np.array([3, 5, 7])]  # Example expected values
    result = akima_interpolate(xi, yi, x, der)
    for res, expected in zip(result, expected_values):
        np.testing.assert_allclose(res, expected)

def test_akima_interpolate_invalid_xi_length():
    xi = np.array([1, 2])
    yi = np.array([1, 4, 9])
    x = 2.5
    with pytest.raises(ValueError):
        akima_interpolate(xi, yi, x)

def test_akima_interpolate_invalid_x():
    xi = np.array([1, 2, 3])
    yi = np.array([1, 4, 9])
    x = np.array([2.5, 3.5])
    der = 0
    result = akima_interpolate(xi, yi, x, der)
    assert len(result) == len(x)

def test_akima_interpolate_empty_input():
    xi = np.array([])
    yi = np.array([])
    x = np.array([1])
    with pytest.raises(ValueError):
        akima_interpolate(xi, yi, x)

def test_akima_interpolate_non_numeric_input():
    xi = np.array([1, 2, 3])
    yi = np.array([1, 4, 'invalid'])
    x = 2.5
    with pytest.raises(TypeError):
        akima_interpolate(xi, yi, x)