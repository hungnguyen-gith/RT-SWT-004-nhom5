import pytest

def test_classify_shipment_priority():
    # Normal test cases
    assert classify_shipment_priority(5, 100, 50, False, False, "bronze") == "low"
    assert classify_shipment_priority(15, 300, 150, True, False, "silver") == "high"
    assert classify_shipment_priority(25, 600, 2000, True, True, "gold") == "urgent"
    assert classify_shipment_priority(10, 250, 500, False, True, "bronze") == "normal"

    # Boundary test cases
    assert classify_shipment_priority(10, 200, 100, False, False, "bronze") == "normal"
    assert classify_shipment_priority(20, 500, 1000, False, False, "bronze") == "normal"
    assert classify_shipment_priority(21, 501, 1001, True, True, "gold") == "urgent"
    assert classify_shipment_priority(10, 201, 101, False, False, "bronze") == "normal"

    # Edge cases
    assert classify_shipment_priority(0, 0, 0, False, False, "bronze") == "low"
    assert classify_shipment_priority(0, 0, 1001, True, True, "gold") == "urgent"
    assert classify_shipment_priority(20, 0, 0, False, False, "bronze") == "low"
    assert classify_shipment_priority(20, 0, 1001, True, True, "gold") == "urgent"
    assert classify_shipment_priority(5, 1000, 100, True, True, "silver") == "high"