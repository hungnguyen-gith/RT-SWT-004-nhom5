def classify_shipment_priority(weight_kg, distance_km, value_usd, is_perishable, is_fragile, customer_tier):
    score = 0
    if weight_kg > 20:
        score += 1
    elif weight_kg > 10:
        score += 2
    else:
        score += 3
    if distance_km > 500:
        score -= 2
    elif distance_km > 200:
        score -= 1
    if value_usd > 1000:
        score += 3
    elif value_usd > 100:
        score += 1
    if is_perishable:
        score += 4
    if is_fragile:
        score += 1
    if customer_tier == "gold":
        score += 2
    elif customer_tier == "silver":
        score += 1
    if score >= 8:
        return "urgent"
    elif score >= 5:
        return "high"
    elif score >= 2:
        return "normal"
    else:
        return "low"