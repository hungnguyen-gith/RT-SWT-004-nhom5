import pytest

def test_compute_discount():
    # Normal test cases
    assert compute_discount(100, "gold") == 85.0
    assert compute_discount(100, "silver") == 90.0
    assert compute_discount(100, "bronze") == 95.0
    assert compute_discount(100, "gold", "SALE") == 80.0
    assert compute_discount(100, "silver", "VIP") == 80.0
    assert compute_discount(100, "bronze", is_first_order=True) == 90.0

    # Boundary test cases
    assert compute_discount(0, "gold") == 0.0
    assert compute_discount(0, "silver") == 0.0
    assert compute_discount(0, "bronze") == 0.0
    assert compute_discount(100, "gold", coupon="SALE") == 80.0
    assert compute_discount(100, "silver", coupon="VIP") == 80.0

    # Edge cases
    assert compute_discount(100, "gold", coupon="INVALID") == 85.0
    assert compute_discount(100, "gold", coupon="SALE", is_first_order=True) == 80.0
    assert compute_discount(100, "gold", coupon="VIP", is_first_order=True) == 75.0
    assert compute_discount(100, "gold", coupon="SALE", is_first_order=False) == 80.0
    assert compute_discount(100, "silver", coupon="SALE", is_first_order=True) == 85.0
    assert compute_discount(100, "silver", coupon="VIP", is_first_order=True) == 80.0
    assert compute_discount(100, "bronze", coupon="SALE", is_first_order=True) == 85.0
    assert compute_discount(100, "bronze", coupon="VIP", is_first_order=True) == 80.0
    assert compute_discount(100, "gold", coupon="SALE", is_first_order=True) == 80.0
    assert compute_discount(100, "gold", coupon="VIP", is_first_order=True) == 75.0
    assert compute_discount(100, "gold", coupon="SALE", is_first_order=False) == 80.0
    assert compute_discount(100, "silver", coupon="SALE", is_first_order=False) == 85.0
    assert compute_discount(100, "bronze", coupon="SALE", is_first_order=False) == 90.0
    assert compute_discount(100, "gold", coupon="VIP", is_first_order=False) == 75.0
    assert compute_discount(100, "silver", coupon="VIP", is_first_order=False) == 80.0
    assert compute_discount(100, "bronze", coupon="VIP", is_first_order=False) == 85.0