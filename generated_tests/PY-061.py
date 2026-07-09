import pytest

def test_truck_heavy_day_no_toll_pass():
    result = resolve_route(0, 100, "heavy", "truck", False, False)
    assert result == {"time": 300.0, "toll": 50, "label": "long"}

def test_truck_light_night_no_toll_pass():
    result = resolve_route(0, 100, "light", "truck", False, True)
    assert result == {"time": 135.0, "toll": 50, "label": "medium"}

def test_motorbike_moderate_day_no_toll_pass():
    result = resolve_route(0, 100, "moderate", "motorbike", False, False)
    assert result == {"time": 104.0, "toll": 5, "label": "short"}

def test_car_heavy_day_with_toll_pass():
    result = resolve_route(0, 100, "heavy", "car", True, False)
    assert result == {"time": 200.0, "toll": 0, "label": "long"}

def test_car_light_night_with_toll_pass():
    result = resolve_route(0, 100, "light", "car", True, True)
    assert result == {"time": 95.0, "toll": 0, "label": "short"}

def test_motorbike_moderate_night_no_toll_pass():
    result = resolve_route(0, 100, "moderate", "motorbike", False, True)
    assert result == {"time": 78.4, "toll": 5, "label": "short"}

def test_truck_moderate_day_with_toll_pass():
    result = resolve_route(0, 100, "moderate", "truck", True, False)
    assert result == {"time": 195.0, "toll": 0, "label": "long"}

def test_car_moderate_night_no_toll_pass():
    result = resolve_route(0, 100, "moderate", "car", False, True)
    assert result == {"time": 123.5, "toll": 20, "label": "long"}

def test_motorbike_heavy_night_no_toll_pass():
    result = resolve_route(0, 100, "heavy", "motorbike", False, True)
    assert result == {"time": 152.0, "toll": 5, "label": "long"}