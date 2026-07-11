import pytest

def test_detect_anomaly_normal_cases():
    assert detect_anomaly([1, 2, 3, 4, 5], 3, 0.5, 2, False) == []
    assert detect_anomaly([1, 2, 3, 10, 5], 3, 0.5, 2, False) == [(3, "high")]
    assert detect_anomaly([10, 9, 8, 7, 6], 8, 0.5, 2, False) == [(0, "low")]
    assert detect_anomaly([1, 2, 3, 4, 5], 3, 0.5, 2, True) == []

def test_detect_anomaly_boundary_cases():
    assert detect_anomaly([3, 3, 3], 3, 0.0, 1, False) == []
    assert detect_anomaly([3, 3, 3], 3, 0.0, 2, False) == []
    assert detect_anomaly([3, 4, 5], 3, 0.5, 1, False) == [(2, "high")]
    assert detect_anomaly([3, 2, 1], 3, 0.5, 1, False) == [(2, "low")]

def test_detect_anomaly_edge_cases():
    assert detect_anomaly([], 3, 0.5, 2, False) == []
    assert detect_anomaly([0], 0, 0.5, 1, False) == []
    assert detect_anomaly([1, 2, 3, 4, 5], 0, 0.5, 2, False) == [(0, "high"), (1, "high"), (2, "high"), (3, "high"), (4, "high")]
    assert detect_anomaly([1, 2, 3, 4, 5], 0, 0.5, 2, True) == [(0, "high"), (1, "high"), (2, "high"), (3, "high"), (4, "high")]

def test_detect_anomaly_with_smoothing():
    assert detect_anomaly([1, 2, 3, 10, 5], 3, 0.5, 2, False, smoothing=True) == [(3, "high")]
    assert detect_anomaly([1, 2, 3, 10, 5], 3, 0.5, 2, False, smoothing=False) == [(3, "high")]
    assert detect_anomaly([1, 2, 3, 4, 5], 3, 0.5, 2, False, smoothing=True) == []
    assert detect_anomaly([1, 2, 3, 4, 5], 3, 0.5, 2, True, smoothing=True) == []