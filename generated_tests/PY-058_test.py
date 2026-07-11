import pytest

def test_compute_loan_eligibility():
    # Normal test cases
    assert compute_loan_eligibility(5000, 700, 2000, 2, 30, True) == True
    assert compute_loan_eligibility(3000, 650, 1000, 1, 25, False) == False
    assert compute_loan_eligibility(4000, 600, 2500, 4, 40, True) == False
    assert compute_loan_eligibility(6000, 750, 1000, 5, 35, True) == True

    # Boundary test cases
    assert compute_loan_eligibility(0, 700, 0, 2, 30, True) == False  # income = 0
    assert compute_loan_eligibility(5000, 500, 2000, 2, 30, True) == False  # credit_score = 500
    assert compute_loan_eligibility(5000, 750, 2000, 2, 30, True) == True  # credit_score = 750
    assert compute_loan_eligibility(5000, 650, 2500, 1, 30, True) == False  # employment_years = 1, credit_score < 700
    assert compute_loan_eligibility(5000, 600, 2000, 2, 30, True) == False  # employment_years = 2, credit_score < 600

    # Edge cases
    assert compute_loan_eligibility(5000, 700, 3000, 2, 30, False) == False  # debt_ratio > 0.5, no collateral
    assert compute_loan_eligibility(5000, 600, 1000, 2, 30, True) == True  # debt_ratio <= 0.2, has collateral
    assert compute_loan_eligibility(5000, 650, 2000, 2, 30, True) == True  # debt_ratio <= 0.4, has collateral
    assert compute_loan_eligibility(5000, 650, 3000, 2, 30, False) == False  # debt_ratio > 0.4, no collateral
    assert compute_loan_eligibility(5000, 700, 2500, 0, 30, True) == False  # employment_years = 0
    assert compute_loan_eligibility(5000, 700, 2500, 3, 17, True) == False  # age < 18
    assert compute_loan_eligibility(5000, 700, 2500, 3, 71, True) == False  # age > 70