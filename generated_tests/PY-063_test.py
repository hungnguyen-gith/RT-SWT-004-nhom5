import pytest

def test_compute_tax_bracket():
    # Normal test cases
    assert compute_tax_bracket(50000, "single", 10000, 0, False) == 6750.0
    assert compute_tax_bracket(30000, "married", 5000, 1, False) == 3750.0
    assert compute_tax_bracket(15000, "single", 2000, 0, True) == 1300.0
    assert compute_tax_bracket(60000, "married", 20000, 2, True) == 5700.0

    # Boundary test cases
    assert compute_tax_bracket(10000, "single", 0, 0, False) == 1000.0
    assert compute_tax_bracket(40000, "single", 0, 0, False) == 5250.0
    assert compute_tax_bracket(90000, "single", 0, 0, False) == 18750.0
    assert compute_tax_bracket(20000, "married", 0, 0, False) == 2000.0
    assert compute_tax_bracket(80000, "married", 0, 0, False) == 10500.0

    # Edge cases
    assert compute_tax_bracket(0, "single", 0, 0, False) == 0.0
    assert compute_tax_bracket(0, "married", 0, 0, False) == 0.0
    assert compute_tax_bracket(0, "single", 0, 0, True) == 0.0
    assert compute_tax_bracket(2000, "single", 2000, 0, False) == 0.0
    assert compute_tax_bracket(2000, "single", 2000, 0, True) == 0.0
    assert compute_tax_bracket(15000, "single", 2000, 0, True) == 1300.0
    assert compute_tax_bracket(20000, "married", 20000, 0, True) == 0.0