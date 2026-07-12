from functions.PY_053 import calculate_shipping

def test_calculate_shipping_normal():
    assert calculate_shipping(1, 50) == 5.0
    assert calculate_shipping(2, 50) == 6.5
    assert calculate_shipping(1, 150) == 6.0
    assert calculate_shipping(2, 150) == 7.5
    assert calculate_shipping(3, 200) == 9.0

def test_calculate_shipping_express():
    assert calculate_shipping(1, 50, express=True) == 7.5
    assert calculate_shipping(2, 50, express=True) == 9.75
    assert calculate_shipping(1, 150, express=True) == 9.0
    assert calculate_shipping(2, 150, express=True) == 11.25
    assert calculate_shipping(3, 200, express=True) == 13.5

def test_calculate_shipping_fragile():
    assert calculate_shipping(1, 50, fragile=True) == 8.0
    assert calculate_shipping(2, 50, fragile=True) == 10.5
    assert calculate_shipping(1, 150, fragile=True) == 9.5
    assert calculate_shipping(2, 150, fragile=True) == 11.75
    assert calculate_shipping(3, 200, fragile=True) == 12.0

def test_calculate_shipping_international():
    assert calculate_shipping(1, 50, country="international") == 10.0
    assert calculate_shipping(2, 50, country="international") == 12.5
    assert calculate_shipping(1, 150, country="international") == 12.0
    assert calculate_shipping(2, 150, country="international") == 15.0
    assert calculate_shipping(3, 200, country="international") == 18.0

def test_calculate_shipping_regional():
    assert calculate_shipping(1, 50, country="regional") == 6.0
    assert calculate_shipping(2, 50, country="regional") == 7.8
    assert calculate_shipping(1, 150, country="regional") == 7.2
    assert calculate_shipping(2, 150, country="regional") == 9.0
    assert calculate_shipping(3, 200, country="regional") == 10.8

def test_calculate_shipping_edge_cases():
    assert calculate_shipping(1, 0) == 5.0
    assert calculate_shipping(1, 100) == 5.0
    assert calculate_shipping(1, 101) == 5.02
    assert calculate_shipping(0, 50) == 5.0
    assert calculate_shipping(0, 0) == 5.0
    assert calculate_shipping(100, 100) == 200.0

def test_calculate_shipping_invalid_input():
    import pytest
    with pytest.raises(TypeError):
        calculate_shipping("a", 50)
    with pytest.raises(TypeError):
        calculate_shipping(1, "b")
    with pytest.raises(TypeError):
        calculate_shipping(1, 50, express="yes")
    with pytest.raises(TypeError):
        calculate_shipping(1, 50, fragile="no")
    with pytest.raises(TypeError):
        calculate_shipping(1, 50, country=5)