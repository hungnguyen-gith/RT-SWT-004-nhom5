import pytest

def test_assign_seat_vip_first_class():
    available_seats = [{"class": "first"}, {"class": "economy"}]
    assert assign_seat("John Doe", available_seats, {}, True, 1) == {"class": "first"}

def test_assign_seat_group_adjacent_seats():
    available_seats = [{"adjacent_free": 2}, {"adjacent_free": 0}]
    assert assign_seat("Group", available_seats, {}, False, 3) == {"adjacent_free": 2}

def test_assign_seat_window_preference():
    available_seats = [{"type": "aisle"}, {"type": "window"}]
    preferences = {"window": True}
    assert assign_seat("Jane Doe", available_seats, preferences, False, 1) == {"type": "window"}

def test_assign_seat_aisle_preference():
    available_seats = [{"type": "window"}, {"type": "aisle"}]
    preferences = {"aisle": True}
    assert assign_seat("Jane Doe", available_seats, preferences, False, 1) == {"type": "aisle"}

def test_assign_seat_no_preferences():
    available_seats = [{"type": "window"}, {"type": "aisle"}]
    assert assign_seat("John Doe", available_seats, {}, False, 1) == {"type": "window"}

def test_assign_seat_empty_available_seats():
    assert assign_seat("John Doe", [], {}, False, 1) is None

def test_assign_seat_group_size_one():
    available_seats = [{"adjacent_free": 0}, {"type": "window"}]
    assert assign_seat("John Doe", available_seats, {}, False, 1) == {"adjacent_free": 0}

def test_assign_seat_group_size_two_no_adjacent():
    available_seats = [{"adjacent_free": 0}, {"adjacent_free": 0}]
    assert assign_seat("Group", available_seats, {}, False, 2) == {"adjacent_free": 0}

def test_assign_seat_vip_no_first_class():
    available_seats = [{"class": "economy"}]
    assert assign_seat("John Doe", available_seats, {}, True, 1) == {"class": "economy"}

def test_assign_seat_multiple_preferences():
    available_seats = [{"type": "aisle"}, {"type": "window"}]
    preferences = {"window": True, "aisle": True}
    assert assign_seat("Jane Doe", available_seats, preferences, False, 1) == {"type": "window"}