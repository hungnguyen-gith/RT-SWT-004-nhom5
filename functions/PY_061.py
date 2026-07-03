def resolve_route(start, end, traffic_level, vehicle_type, has_toll_pass, is_night):
    base_time = abs(end - start)
    if vehicle_type == "truck":
        base_time *= 1.5
    elif vehicle_type == "motorbike":
        base_time *= 0.8
    if traffic_level == "heavy":
        base_time *= 2.0
    elif traffic_level == "moderate":
        base_time *= 1.3
    elif traffic_level == "light":
        base_time *= 1.0
    if is_night:
        if vehicle_type == "truck":
            base_time *= 0.9
        else:
            base_time *= 0.95
    toll_cost = 0
    if not has_toll_pass:
        if vehicle_type == "truck":
            toll_cost = 50
        elif vehicle_type == "car":
            toll_cost = 20
        else:
            toll_cost = 5
    if base_time > 120:
        route_label = "long"
    elif base_time > 60:
        route_label = "medium"
    else:
        route_label = "short"
    return {"time": base_time, "toll": toll_cost, "label": route_label}