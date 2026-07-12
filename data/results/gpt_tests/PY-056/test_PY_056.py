import pytest

def classify_shipment_priority(weight_kg, distance_km, value_usd, is_perishable, is_fragile, customer_tier):
    score = 0

    if weight_kg > 20:
        score += 1
    elif weight_kg > 10:
        score += 2
    else:
        score += 3

    if distance_km > 500:
        score -= 2
    elif distance_km > 200:
        score -= 1

    if value_usd > 1000:
        score += 3
    elif value_usd > 100:
        score += 1

    if is_perishable:
        score += 4

    if is_fragile:
        score += 1

    if customer_tier == "gold":
        score += 2
    elif customer_tier == "silver":
        score += 1

    if score >= 8:
        return "urgent"
    elif score >= 5:
        return "high"
    elif score >= 2:
        return "normal"
    else:
        return "low"

def test_classify_shipment_priority():
    # Normal test cases
    assert classify_shipment_priority(5, 100, 150, False, False, "bronze") == "normal"
    assert classify_shipment_priority(15, 300, 500, True, True, "silver") == "high"
    assert classify_shipment_priority(25, 600, 1200, False, True, "gold") == "urgent"
    
    # Boundary test cases
    assert classify_shipment_priority(10, 200, 100, False, False, "bronze") == "normal"
    assert classify_shipment_priority(20, 500, 1000, False, False, "bronze") == "normal"
    assert classify_shipment_priority(21, 501, 1001, True, True, "gold") == "urgent"
    
    # Edge cases
    assert classify_shipment_priority(0, 0, 0, False, False, "bronze") == "low"
    assert classify_shipment_priority(10, 201, 101, True, False, "silver") == "high"
    assert classify_shipment_priority(10, 201, 101, False, True, "gold") == "high"
    assert classify_shipment_priority(10, 201, 100, False, False, "silver") == "normal"
    assert classify_shipment_priority(10, 201, 100, True, True, "gold") == "high"