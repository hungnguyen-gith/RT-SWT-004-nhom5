import pytest

def test_assign_seat_vip_first_class():
    passenger = "John Doe"
    available_seats = [{"class": "first"}, {"class": "economy"}]
    preferences = {}
    is_vip = True
    group_size = 1
    assert assign_seat(passenger, available_seats, preferences, is_vip, group_size) == {"class": "first"}

def test_assign_seat_group_size_adjacent():
    passenger = "Jane Doe"
    available_seats = [{"adjacent_free": 2}, {"adjacent_free": 0}]
    preferences = {}
    is_vip = False
    group_size = 2
    assert assign_seat(passenger, available_seats, preferences, is_vip, group_size) == {"adjacent_free": 2}

def test_assign_seat_window_preference():
    passenger = "Alice"
    available_seats = [{"type": "aisle"}, {"type": "window"}]
    preferences = {"window": True}
    is_vip = False
    group_size = 1
    assert assign_seat(passenger, available_seats, preferences, is_vip, group_size) == {"type": "window"}

def test_assign_seat_aisle_preference():
    passenger = "Bob"
    available_seats = [{"type": "window"}, {"type": "aisle"}]
    preferences = {"aisle": True}
    is_vip = False
    group_size = 1
    assert assign_seat(passenger, available_seats, preferences, is_vip, group_size) == {"type": "aisle"}

def test_assign_seat_no_preferences():
    passenger = "Charlie"
    available_seats = [{"type": "window"}, {"type": "aisle"}]
    preferences = {}
    is_vip = False
    group_size = 1
    assert assign_seat(passenger, available_seats, preferences, is_vip, group_size) == {"type": "window"}

def test_assign_seat_empty_available_seats():
    passenger = "Diana"
    available_seats = []
    preferences = {}
    is_vip = False
    group_size = 1
    assert assign_seat(passenger, available_seats, preferences, is_vip, group_size) is None

def test_assign_seat_group_size_one_no_adjacent():
    passenger = "Eve"
    available_seats = [{"adjacent_free": 0}]
    preferences = {}
    is_vip = False
    group_size = 1
    assert assign_seat(passenger, available_seats, preferences, is_vip, group_size) == {"adjacent_free": 0}