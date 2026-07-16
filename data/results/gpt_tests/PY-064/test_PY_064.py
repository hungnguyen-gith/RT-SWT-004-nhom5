import pytest

def test_detect_anomaly_normal_cases():
    assert detect_anomaly([1, 2, 3, 4, 5], 3, 0.5, 2, False) == []
    assert detect_anomaly([1, 2, 3, 4, 10], 3, 0.5, 2, False) == [(4, "high")]
    assert detect_anomaly([10, 9, 8, 7, 1], 5, 0.5, 2, False) == [(0, "low")]

def test_detect_anomaly_boundary_cases():
    assert detect_anomaly([1, 1, 1, 1, 1], 1, 0.0, 1, False) == []
    assert detect_anomaly([1, 1, 1, 1, 2], 1, 0.0, 1, False) == [(4, "high")]
    assert detect_anomaly([1, 1, 1, 1, 0], 1, 0.0, 1, False) == [(4, "low")]

def test_detect_anomaly_edge_cases():
    assert detect_anomaly([], 1, 0.5, 2, False) == []
    assert detect_anomaly([0], 0, 0.5, 1, False) == []
    assert detect_anomaly([1, 2, 3, 4, 5], 0, 0.5, 2, False) == [(0, "high"), (1, "high"), (2, "high"), (3, "high"), (4, "high")]
    assert detect_anomaly([1, 2, 3, 4, 5], 0, 0.5, 2, True) == [(0, "high"), (1, "high"), (2, "high"), (3, "high"), (4, "high")]

def test_detect_anomaly_with_smoothing():
    assert detect_anomaly([1, 2, 3, 4, 10], 3, 0.5, 2, False, smoothing=True) == [(4, "high")]
    assert detect_anomaly([1, 2, 3, 4, 10], 3, 0.5, 2, False, smoothing=False) == [(4, "high")]
    assert detect_anomaly([1, 2, 3, 4, 10], 3, 0.5, 2, True, smoothing=True) == [(4, "high")]

def test_detect_anomaly_with_negative_spike():
    assert detect_anomaly([1, 2, 3, 4, -10], 3, 0.5, 2, True) == []
    assert detect_anomaly([1, 2, 3, 4, -10], 3, 0.5, 2, False) == [(4, "low")]