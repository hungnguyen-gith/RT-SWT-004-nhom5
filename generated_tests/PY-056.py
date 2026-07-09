import pytest

def test_classify_shipment_priority():
    assert classify_shipment_priority(5, 100, 50, False, False, "bronze") == "low"
    assert classify_shipment_priority(15, 300, 150, True, False, "silver") == "high"
    assert classify_shipment_priority(25, 600, 2000, True, True, "gold") == "urgent"
    assert classify_shipment_priority(10, 250, 500, False, True, "silver") == "normal"
    assert classify_shipment_priority(30, 100, 800, False, False, "bronze") == "normal"
    assert classify_shipment_priority(20, 700, 1200, True, True, "gold") == "urgent"
    assert classify_shipment_priority(8, 150, 90, False, False, "bronze") == "low"
    assert classify_shipment_priority(12, 400, 1100, True, True, "silver") == "high"
    assert classify_shipment_priority(22, 250, 300, False, True, "gold") == "normal"
    assert classify_shipment_priority(0, 0, 0, False, False, "bronze") == "low"