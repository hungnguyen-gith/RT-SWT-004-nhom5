import pytest

def test_calculate_shipping_normal_cases():
    assert calculate_shipping(1, 50) == 5.0
    assert calculate_shipping(2, 50) == 6.5
    assert calculate_shipping(1, 150) == 5.5
    assert calculate_shipping(2, 150) == 7.0
    assert calculate_shipping(2, 150, express=True) == 10.5
    assert calculate_shipping(2, 150, fragile=True) == 10.0
    assert calculate_shipping(2, 150, express=True, fragile=True) == 13.5
    assert calculate_shipping(2, 150, country="international") == 14.0
    assert calculate_shipping(2, 150, country="regional") == 8.4

def test_calculate_shipping_boundary_cases():
    assert calculate_shipping(1, 50) == 5.0
    assert calculate_shipping(1, 51) == 5.01
    assert calculate_shipping(1, 100) == 5.0
    assert calculate_shipping(1, 101) == 5.02
    assert calculate_shipping(1, 100, express=True) == 7.5
    assert calculate_shipping(1, 100, fragile=True) == 8.0
    assert calculate_shipping(1, 100, express=True, fragile=True) == 10.5

def test_calculate_shipping_edge_cases():
    assert calculate_shipping(0, 0) == 5.0
    assert calculate_shipping(0, 50) == 5.0
    assert calculate_shipping(1, 0) == 5.0
    assert calculate_shipping(1, 1) == 5.0
    assert calculate_shipping(1, 50, express=True) == 7.5
    assert calculate_shipping(1, 50, fragile=True) == 8.0
    assert calculate_shipping(1, 50, express=True, fragile=True) == 10.5
    assert calculate_shipping(1, 200) == 5.0 + (200 - 100) * 0.02
    assert calculate_shipping(1, 200, country="international") == (5.0 + (200 - 100) * 0.02) * 2.0

def test_calculate_shipping_limit_cases():
    assert calculate_shipping(100, 100) == 200.0
    assert calculate_shipping(100, 200) == 200.0
    assert calculate_shipping(100, 100, express=True) == 200.0
    assert calculate_shipping(100, 100, fragile=True) == 200.0
    assert calculate_shipping(100, 100, express=True, fragile=True) == 200.0
    assert calculate_shipping(100, 100, country="international") == 200.0
    assert calculate_shipping(100, 100, country="regional") == 200.0