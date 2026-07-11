import pytest
import numpy as np

# Assuming the akima_interpolate function is defined in a module named 'interpolation'
from interpolation import akima_interpolate

def test_akima_interpolate_normal_cases():
    xi = np.array([1, 2, 3, 4, 5])
    yi = np.array([2, 3, 5, 4, 6])
    x = np.array([1.5, 2.5, 3.5])
    expected = np.array([2.5, 4.0, 4.5])
    result = akima_interpolate(xi, yi, x)
    np.testing.assert_almost_equal(result, expected)

def test_akima_interpolate_boundary_cases():
    xi = np.array([0, 1, 2])
    yi = np.array([0, 1, 0])
    x = np.array([0, 2])
    expected = np.array([0, 0])
    result = akima_interpolate(xi, yi, x)
    np.testing.assert_almost_equal(result, expected)

def test_akima_interpolate_edge_case_single_point():
    xi = np.array([1])
    yi = np.array([1])
    x = np.array([1])
    expected = np.array([1])
    result = akima_interpolate(xi, yi, x)
    np.testing.assert_almost_equal(result, expected)

def test_akima_interpolate_edge_case_empty_input():
    xi = np.array([])
    yi = np.array([])
    x = np.array([1])
    with pytest.raises(ValueError):
        akima_interpolate(xi, yi, x)

def test_akima_interpolate_derivative_case():
    xi = np.array([0, 1, 2])
    yi = np.array([0, 1, 0])
    x = np.array([0.5])
    expected_derivative = np.array([-1])
    result = akima_interpolate(xi, yi, x, der=1)
    np.testing.assert_almost_equal(result, expected_derivative)

def test_akima_interpolate_multiple_derivatives():
    xi = np.array([0, 1, 2])
    yi = np.array([0, 1, 0])
    x = np.array([0.5])
    expected = np.array([-1, 0])  # First derivative and second derivative
    result = akima_interpolate(xi, yi, x, der=[1, 2])
    np.testing.assert_almost_equal(result, expected)

def test_akima_interpolate_non_sorted_xi():
    xi = np.array([3, 1, 2])
    yi = np.array([0, 1, 0.5])
    x = np.array([1.5])
    with pytest.raises(ValueError):
        akima_interpolate(xi, yi, x)