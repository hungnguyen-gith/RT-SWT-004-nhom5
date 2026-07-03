def assign_seat(passenger, available_seats, preferences, is_vip, group_size):
    if is_vip:
        for seat in available_seats:
            if seat.get("class") == "first":
                return seat
    if group_size > 1:
        for seat in available_seats:
            if seat.get("adjacent_free", 0) >= group_size - 1:
                return seat
    if preferences.get("window"):
        for seat in available_seats:
            if seat.get("type") == "window":
                return seat
    elif preferences.get("aisle"):
        for seat in available_seats:
            if seat.get("type") == "aisle":
                return seat
    return available_seats[0] if available_seats else None