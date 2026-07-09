import pytest

def test_no_anomalies():
    assert detect_anomaly([100, 100, 100], 100, 0.1, 2, False) == []

def test_high_anomaly():
    assert detect_anomaly([110, 115, 120], 100, 0.1, 2, False) == [(2, "high")]

def test_low_anomaly():
    assert detect_anomaly([90, 85, 80], 100, 0.1, 2, False) == [(2, "low")]

def test_consecutive_anomalies():
    assert detect_anomaly([110, 115, 120, 125], 100, 0.1, 3, False) == [(3, "high")]

def test_reset_on_recovery():
    assert detect_anomaly([110, 115, 100, 105, 110], 100, 0.1, 2, False) == [(1, "high")]

def test_no_reset_on_recovery():
    assert detect_anomaly([110, 115, 100, 105, 110], 100, 0.1, 2, False, reset_on_recovery=False) == [(1, "high")]

def test_allow_negative_spike():
    assert detect_anomaly([110, 105, 100, 95], 100, 0.1, 2, True) == []

def test_smoothing_enabled():
    assert detect_anomaly([110, 120, 130], 100, 0.1, 2, False, smoothing=True) == [(2, "high")]

def test_smoothing_with_recovery():
    assert detect_anomaly([110, 120, 100, 90], 100, 0.1, 2, False, smoothing=True) == [(1, "high")]

def test_baseline_zero():
    assert detect_anomaly([1, 2, 3], 0, 0.1, 2, False) == []