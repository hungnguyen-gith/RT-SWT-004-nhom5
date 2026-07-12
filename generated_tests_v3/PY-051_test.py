from functions.PY_051 import compute_discount

def test_compute_discount_gold_tier():
    assert compute_discount(100, "gold") == 85.0
    assert compute_discount(200, "gold") == 170.0

def test_compute_discount_silver_tier():
    assert compute_discount(100, "silver") == 90.0
    assert compute_discount(200, "silver") == 180.0

def test_compute_discount_bronze_tier():
    assert compute_discount(100, "bronze") == 95.0
    assert compute_discount(200, "bronze") == 190.0

def test_compute_discount_with_coupon_sale():
    assert compute_discount(100, "gold", coupon="SALE") == 80.0
    assert compute_discount(200, "silver", coupon="SALE") == 160.0

def test_compute_discount_with_coupon_vip():
    assert compute_discount(100, "gold", coupon="VIP") == 75.0
    assert compute_discount(200, "silver", coupon="VIP") == 150.0

def test_compute_discount_first_order():
    assert compute_discount(100, "gold", is_first_order=True) == 80.0
    assert compute_discount(200, "silver", is_first_order=True) == 160.0

def test_compute_discount_with_coupon_and_first_order():
    assert compute_discount(100, "gold", coupon="SALE", is_first_order=True) == 75.0
    assert compute_discount(200, "silver", coupon="VIP", is_first_order=True) == 135.0

def test_compute_discount_exceeding_max_discount():
    assert compute_discount(100, "gold", coupon="VIP", is_first_order=True) == 70.0
    assert compute_discount(200, "silver", coupon="VIP", is_first_order=True) == 100.0

def test_compute_discount_invalid_customer_tier():
    assert compute_discount(100, "platinum") == 100.0  # No discount for invalid tier

def test_compute_discount_zero_total():
    assert compute_discount(0, "gold") == 0.0
    assert compute_discount(0, "silver", coupon="SALE") == 0.0

def test_compute_discount_negative_total():
    assert compute_discount(-100, "gold") == -85.0
    assert compute_discount(-200, "silver", coupon="SALE") == -170.0

def test_compute_discount_no_discount():
    assert compute_discount(100, "none") == 100.0  # No discount for no tier or invalid tier