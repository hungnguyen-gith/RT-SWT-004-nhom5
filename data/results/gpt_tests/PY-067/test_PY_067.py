import pytest
import numpy as np

# Assuming the akima_interpolate function is defined in a module named 'interpolation'
from interpolation import akima_interpolate

def test_akima_interpolate_normal_cases():
    xi = np.array([1, 2, 3, 4, 5])
    yi = np.array([2, 3, 5, 4, 6])
    x = np.array([1.5, 2.5, 3.5])
    
    result = akima_interpolate(xi, yi, x)
    expected = np.array([2.5, 4.0, 4.5])
    np.testing.assert_almost_equal(result, expected)

def test_akima_interpolate_boundary_cases():
    xi = np.array([0, 1])
    yi = np.array([0, 1])
    x = np.array([0, 1])
    
    result = akima_interpolate(xi, yi, x)
    expected = np.array([0, 1])
    np.testing.assert_almost_equal(result, expected)

def test_akima_interpolate_edge_cases():
    xi = np.array([1, 2, 3])
    yi = np.array([1, 4, 9])
    x = np.array([0, 1, 4])
    
    result = akima_interpolate(xi, yi, x)
    expected = np.array([1, 1, 9])  # Extrapolation expected
    np.testing.assert_almost_equal(result, expected)

def test_akima_interpolate_derivative_case():
    xi = np.array([1, 2, 3])
    yi = np.array([1, 4, 9])
    x = np.array([1.5])
    der = 1
    
    result = akima_interpolate(xi, yi, x, der)
    expected = np.array([3])  # Derivative at x=1.5
    np.testing.assert_almost_equal(result, expected)

def test_akima_interpolate_multiple_derivatives():
    xi = np.array([1, 2, 3])
    yi = np.array([1, 4, 9])
    x = np.array([1.5])
    der = [0, 1]
    
    result = akima_interpolate(xi, yi, x, der)
    expected = [np.array([2.5]), np.array([3])]  # Value and derivative
    for r, e in zip(result, expected):
        np.testing.assert_almost_equal(r, e)

def test_akima_interpolate_empty_input():
    xi = np.array([])
    yi = np.array([])
    x = np.array([1])
    
    with pytest.raises(ValueError):
        akima_interpolate(xi, yi, x)

def test_akima_interpolate_single_point():
    xi = np.array([1])
    yi = np.array([1])
    x = np.array([1])
    
    result = akima_interpolate(xi, yi, x)
    expected = np.array([1])
    np.testing.assert_almost_equal(result, expected)