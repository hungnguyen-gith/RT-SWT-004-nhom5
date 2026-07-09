import pytest

def test_compute_discount_gold_tier_no_coupon():
    assert compute_discount(100, "gold") == 85.0

def test_compute_discount_silver_tier_no_coupon():
    assert compute_discount(100, "silver") == 90.0

def test_compute_discount_bronze_tier_no_coupon():
    assert compute_discount(100, "bronze") == 95.0

def test_compute_discount_gold_tier_with_sale_coupon():
    assert compute_discount(100, "gold", "SALE123") == 80.0

def test_compute_discount_silver_tier_with_sale_coupon():
    assert compute_discount(100, "silver", "SALE123") == 85.0

def test_compute_discount_bronze_tier_with_sale_coupon():
    assert compute_discount(100, "bronze", "SALE123") == 90.0

def test_compute_discount_gold_tier_with_vip_coupon():
    assert compute_discount(100, "gold", "VIP123") == 75.0

def test_compute_discount_silver_tier_with_vip_coupon():
    assert compute_discount(100, "silver", "VIP123") == 80.0

def test_compute_discount_bronze_tier_with_vip_coupon():
    assert compute_discount(100, "bronze", "VIP123") == 85.0

def test_compute_discount_first_order_gold_tier():
    assert compute_discount(100, "gold", is_first_order=True) == 80.0

def test_compute_discount_first_order_silver_tier():
    assert compute_discount(100, "silver", is_first_order=True) == 85.0

def test_compute_discount_first_order_bronze_tier():
    assert compute_discount(100, "bronze", is_first_order=True) == 90.0

def test_compute_discount_gold_tier_with_coupon_exceeding_limit():
    assert compute_discount(100, "gold", "VIP123", is_first_order=True) == 75.0

def test_compute_discount_no_discount():
    assert compute_discount(100, "none") == 100.0

def test_compute_discount_coupon_exceeding_limit():
    assert compute_discount(100, "gold", "VIP123", is_first_order=True) == 75.0

def test_compute_discount_high_total():
    assert compute_discount(1000, "gold") == 850.0

def test_compute_discount_high_total_with_coupon():
    assert compute_discount(1000, "silver", "SALE123") == 850.0

def test_compute_discount_high_total_first_order():
    assert compute_discount(1000, "bronze", is_first_order=True) == 950.0