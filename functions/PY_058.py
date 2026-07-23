def compute_loan_eligibility(income, credit_score, existing_debt, employment_years, age, has_collateral):

    if age < 18 or age > 70:

        return False

    if credit_score < 500:

        return False

    debt_ratio = existing_debt / income if income > 0 else 1.0

    if debt_ratio > 0.5:

        if not has_collateral:

            return False

        elif credit_score < 650:

            return False

    if employment_years < 1:

        if credit_score < 700:

            return False

    elif employment_years < 3:

        if credit_score < 600:

            return False

    if credit_score >= 750:

        return True

    elif credit_score >= 650:

        return debt_ratio <= 0.4

    else:

        return debt_ratio <= 0.2 and has_collateral
    