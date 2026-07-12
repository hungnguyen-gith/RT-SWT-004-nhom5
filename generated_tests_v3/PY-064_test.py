from functions.PY_064 import detect_anomaly
import pytest

def test_detect_anomaly_normal_cases():
    # Normal high anomaly detection
    readings = [100, 110, 120, 130, 140]
    baseline = 100
    tolerance_pct = 0.2
    min_consecutive = 2
    allow_negative_spike = False
    result = detect_anomaly(readings, baseline, tolerance_pct, min_consecutive, allow_negative_spike)
    assert result == [(3, "high")]

    # Normal low anomaly detection
    readings = [100, 90, 80, 70, 60]
    baseline = 100
    tolerance_pct = 0.2
    min_consecutive = 2
    allow_negative_spike = False
    result = detect_anomaly(readings, baseline, tolerance_pct, min_consecutive, allow_negative_spike)
    assert result == [(3, "low")]

def test_detect_anomaly_edge_cases():
    # Edge case with no anomalies
    readings = [100, 100, 100, 100]
    baseline = 100
    tolerance_pct = 0.2
    min_consecutive = 2
    allow_negative_spike = False
    result = detect_anomaly(readings, baseline, tolerance_pct, min_consecutive, allow_negative_spike)
    assert result == []

    # Edge case with exactly at tolerance
    readings = [100, 120]
    baseline = 100
    tolerance_pct = 0.2
    min_consecutive = 1
    allow_negative_spike = False
    result = detect_anomaly(readings, baseline, tolerance_pct, min_consecutive, allow_negative_spike)
    assert result == [(1, "high")]

def test_detect_anomaly_invalid_input():
    # Invalid input: empty readings
    readings = []
    baseline = 100
    tolerance_pct = 0.2
    min_consecutive = 2
    allow_negative_spike = False
    result = detect_anomaly(readings, baseline, tolerance_pct, min_consecutive, allow_negative_spike)
    assert result == []

    # Invalid input: negative baseline
    readings = [100, 110, 120]
    baseline = -100
    tolerance_pct = 0.2
    min_consecutive = 2
    allow_negative_spike = False
    result = detect_anomaly(readings, baseline, tolerance_pct, min_consecutive, allow_negative_spike)
    assert result == []

def test_detect_anomaly_smoothing():
    # Test with smoothing enabled
    readings = [100, 110, 120, 130, 140]
    baseline = 100
    tolerance_pct = 0.2
    min_consecutive = 2
    allow_negative_spike = False
    smoothing = True
    result = detect_anomaly(readings, baseline, tolerance_pct, min_consecutive, allow_negative_spike, smoothing=smoothing)
    assert result == [(3, "high")]

def test_detect_anomaly_reset_on_recovery():
    # Test with reset_on_recovery set to False
    readings = [100, 110, 120, 90, 80, 70]
    baseline = 100
    tolerance_pct = 0.2
    min_consecutive = 2
    allow_negative_spike = False
    reset_on_recovery = False
    result = detect_anomaly(readings, baseline, tolerance_pct, min_consecutive, allow_negative_spike, reset_on_recovery=reset_on_recovery)
    assert result == [(2, "high"), (5, "low")]  # Should detect high and low anomalies

def test_detect_anomaly_allow_negative_spike():
    # Test with allow_negative_spike set to True
    readings = [100, 110, 120, 90, 80, 70]
    baseline = 100
    tolerance_pct = 0.2
    min_consecutive = 2
    allow_negative_spike = True
    result = detect_anomaly(readings, baseline, tolerance_pct, min_consecutive, allow_negative_spike)
    assert result == [(2, "high")]  # Should only detect high anomaly