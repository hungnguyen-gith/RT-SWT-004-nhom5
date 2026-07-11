def detect_anomaly(readings, baseline, tolerance_pct, min_consecutive, allow_negative_spike, smoothing=False, reset_on_recovery=True):
    anomalies = []
    consecutive = 0
    prev_value = None
    for i, value in enumerate(readings):
        if smoothing and prev_value is not None:
            value = (value + prev_value) / 2
        deviation = (value - baseline) / baseline if baseline != 0 else 0
        is_high = deviation > tolerance_pct
        is_low = deviation < -tolerance_pct and not allow_negative_spike
        if is_high or is_low:
            consecutive += 1
            if consecutive >= min_consecutive:
                if is_high:
                    anomalies.append((i, "high"))
                elif is_low:
                    anomalies.append((i, "low"))
        else:
            if reset_on_recovery:
                consecutive = 0
            elif consecutive > 0:
                consecutive -= 1
        prev_value = value
    return anomalies