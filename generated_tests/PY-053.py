import pytest

def test_calculate_shipping_base_case():
    assert calculate_shipping(1, 50) == 5.0

def test_calculate_shipping_weight_case():
    assert calculate_shipping(2, 50) == 6.5
    assert calculate_shipping(3, 50) == 8.0

def test_calculate_shipping_distance_case():
    assert calculate_shipping(1, 51) == 5.01
    assert calculate_shipping(1, 101) == 5.02

def test_calculate_shipping_express_case():
    assert calculate_shipping(1, 50, express=True) == 7.5
    assert calculate_shipping(2, 50, express=True) == 9.75

def test_calculate_shipping_fragile_case():
    assert calculate_shipping(1, 50, fragile=True) == 8.0
    assert calculate_shipping(2, 50, fragile=True) == 10.5

def test_calculate_shipping_international_case():
    assert calculate_shipping(1, 50, country="international") == 10.0
    assert calculate_shipping(2, 50, country="international") == 13.0

def test_calculate_shipping_regional_case():
    assert calculate_shipping(1, 50, country="regional") == 6.0
    assert calculate_shipping(2, 50, country="regional") == 7.8

def test_calculate_shipping_high_weight():
    assert calculate_shipping(100, 50) == 152.0

def test_calculate_shipping_high_distance():
    assert calculate_shipping(1, 200) == 10.0

def test_calculate_shipping_high_base_case():
    assert calculate_shipping(100, 100) == 200.0

def test_calculate_shipping_combined_cases():
    assert calculate_shipping(3, 150, express=True, fragile=True, country="international") == 200.0
    assert calculate_shipping(2, 75, express=False, fragile=False, country="regional") == 8.4