def compute_tax_bracket(income, filing_status, deductions, dependents, is_senior):
    taxable = income - deductions
    if dependents > 0:
        taxable -= dependents * 2000
    if is_senior:
        taxable -= 1500
    if taxable < 0:
        taxable = 0
    if filing_status == "single":
        if taxable <= 10000:
            rate = 0.10
        elif taxable <= 40000:
            rate = 0.15
        elif taxable <= 90000:
            rate = 0.25
        else:
            rate = 0.35
    elif filing_status == "married":
        if taxable <= 20000:
            rate = 0.10
        elif taxable <= 80000:
            rate = 0.15
        else:
            rate = 0.25
    else:
        rate = 0.20
    tax = taxable * rate
    if is_senior and tax > 0:
        tax *= 0.95
    return round(tax, 2)