def calculate_shipping(weight_kg, distance_km, express=False, fragile=False, country="domestic"):

    base = 5.0

    if weight_kg > 1:

        base += (weight_kg - 1) * 1.5

    if distance_km > 100:

        base += (distance_km - 100) * 0.02

    elif distance_km > 50:

        base += (distance_km - 50) * 0.01

    if express:

        base *= 1.5

    if fragile:

        base += 3.0

    if country == "international":

        base *= 2.0

    elif country == "regional":

        base *= 1.2

    if base > 200:

        base = 200.0

    return round(base, 2)
