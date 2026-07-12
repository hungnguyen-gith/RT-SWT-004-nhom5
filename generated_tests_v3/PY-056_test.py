from functions.PY_056 import classify_shipment_priority

def test_classify_shipment_priority():
    # Test normal cases
    assert classify_shipment_priority(5, 100, 50, False, False, "bronze") == "low"
    assert classify_shipment_priority(15, 300, 150, True, False, "silver") == "high"
    assert classify_shipment_priority(25, 600, 1200, True, True, "gold") == "urgent"
    assert classify_shipment_priority(10, 250, 200, False, True, "bronze") == "normal"

    # Test edge cases
    assert classify_shipment_priority(20, 500, 1000, False, False, "bronze") == "normal"
    assert classify_shipment_priority(20, 501, 1000, False, False, "bronze") == "low"
    assert classify_shipment_priority(10, 201, 100, False, False, "bronze") == "low"
    assert classify_shipment_priority(10, 200, 101, False, False, "bronze") == "normal"

    # Test maximum values
    assert classify_shipment_priority(100, 1000, 5000, True, True, "gold") == "urgent"
    assert classify_shipment_priority(100, 1000, 5000, False, False, "silver") == "high"

    # Test invalid inputs
    assert classify_shipment_priority(-1, 100, 50, False, False, "bronze") == "low"
    assert classify_shipment_priority(5, -100, 50, False, False, "bronze") == "low"
    assert classify_shipment_priority(5, 100, -50, False, False, "bronze") == "low"
    assert classify_shipment_priority(5, 100, 50, None, False, "bronze") == "low"
    assert classify_shipment_priority(5, 100, 50, False, None, "bronze") == "low"
    assert classify_shipment_priority(5, 100, 50, False, False, None) == "low"