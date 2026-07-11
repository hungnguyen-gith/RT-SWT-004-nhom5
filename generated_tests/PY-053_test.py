import pytest

def test_calculate_shipping_normal_cases():
    assert calculate_shipping(1, 50) == 5.0
    assert calculate_shipping(2, 50) == 6.5
    assert calculate_shipping(1, 150) == 5.5
    assert calculate_shipping(2, 150) == 7.0
    assert calculate_shipping(3, 200, express=True) == 10.5
    assert calculate_shipping(1, 200, fragile=True) == 8.0
    assert calculate_shipping(2, 200, express=True, fragile=True) == 12.0
    assert calculate_shipping(1, 200, country="international") == 10.0
    assert calculate_shipping(2, 200, country="regional") == 9.0

def test_calculate_shipping_boundary_cases():
    assert calculate_shipping(1, 50) == 5.0
    assert calculate_shipping(1, 51) == 5.01
    assert calculate_shipping(1, 100) == 5.5
    assert calculate_shipping(1, 101) == 5.52
    assert calculate_shipping(1, 200) == 10.0
    assert calculate_shipping(1, 201) == 10.02
    assert calculate_shipping(1, 100, express=True) == 8.25
    assert calculate_shipping(1, 100, fragile=True) == 8.5

def test_calculate_shipping_edge_cases():
    assert calculate_shipping(0, 0) == 5.0
    assert calculate_shipping(0, 50) == 5.0
    assert calculate_shipping(1, 0) == 5.0
    assert calculate_shipping(1, 1) == 5.0
    assert calculate_shipping(1, 50, express=True) == 7.5
    assert calculate_shipping(1, 50, fragile=True) == 8.0
    assert calculate_shipping(1, 50, express=True, fragile=True) == 10.5
    assert calculate_shipping(1, 50, country="international") == 10.0
    assert calculate_shipping(1, 50, country="regional") == 6.0
    assert calculate_shipping(1, 200, country="international") == 10.0
    assert calculate_shipping(1, 200, country="regional") == 9.0