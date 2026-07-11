def compute_discount(total, customer_tier, coupon=None, is_first_order=False):
    rate = 0.0
    if customer_tier == "gold":
        rate = 0.15
    elif customer_tier == "silver":
        rate = 0.10
    elif customer_tier == "bronze":
        rate = 0.05
    if coupon:
        if coupon.startswith("SALE"):
            rate += 0.05
        elif coupon.startswith("VIP"):
            rate += 0.10
    if is_first_order:
        rate += 0.05
    if rate > 0.5:
        rate = 0.5
    return total * (1 - rate)