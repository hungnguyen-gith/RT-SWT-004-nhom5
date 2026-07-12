from functions.PY_065 import assign_seat

class StubPassenger:
    def __init__(self):
        self.name = "Test Passenger"
        self.id = 1

def test_assign_seat_vip_first_class():
    passenger = StubPassenger()
    available_seats = [{"class": "economy"}, {"class": "first"}]
    preferences = {}
    is_vip = True
    group_size = 1

    result = assign_seat(passenger, available_seats, preferences, is_vip, group_size)
    assert result == {"class": "first"}

def test_assign_seat_group_size_adjacent():
    passenger = StubPassenger()
    available_seats = [
        {"class": "economy", "adjacent_free": 2},
        {"class": "economy", "adjacent_free": 0}
    ]
    preferences = {}
    is_vip = False
    group_size = 3

    result = assign_seat(passenger, available_seats, preferences, is_vip, group_size)
    assert result == {"class": "economy", "adjacent_free": 2}

def test_assign_seat_window_preference():
    passenger = StubPassenger()
    available_seats = [
        {"class": "economy", "type": "aisle"},
        {"class": "economy", "type": "window"}
    ]
    preferences = {"window": True}
    is_vip = False
    group_size = 1

    result = assign_seat(passenger, available_seats, preferences, is_vip, group_size)
    assert result == {"class": "economy", "type": "window"}

def test_assign_seat_aisle_preference():
    passenger = StubPassenger()
    available_seats = [
        {"class": "economy", "type": "window"},
        {"class": "economy", "type": "aisle"}
    ]
    preferences = {"aisle": True}
    is_vip = False
    group_size = 1

    result = assign_seat(passenger, available_seats, preferences, is_vip, group_size)
    assert result == {"class": "economy", "type": "aisle"}

def test_assign_seat_no_available_seats():
    passenger = StubPassenger()
    available_seats = []
    preferences = {}
    is_vip = False
    group_size = 1

    result = assign_seat(passenger, available_seats, preferences, is_vip, group_size)
    assert result is None

def test_assign_seat_no_preferences():
    passenger = StubPassenger()
    available_seats = [{"class": "economy"}]
    preferences = {}
    is_vip = False
    group_size = 1

    result = assign_seat(passenger, available_seats, preferences, is_vip, group_size)
    assert result == {"class": "economy"}