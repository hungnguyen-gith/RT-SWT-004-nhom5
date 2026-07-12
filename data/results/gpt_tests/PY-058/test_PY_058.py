import pytest

def test_compute_loan_eligibility():
    # Normal test cases
    assert compute_loan_eligibility(5000, 700, 2000, 2, 30, True) == True
    assert compute_loan_eligibility(4000, 650, 1500, 1, 25, False) == False
    assert compute_loan_eligibility(3000, 600, 2000, 4, 40, True) == False
    assert compute_loan_eligibility(6000, 800, 1000, 5, 35, True) == True

    # Boundary test cases
    assert compute_loan_eligibility(0, 700, 0, 2, 30, True) == False  # income = 0
    assert compute_loan_eligibility(5000, 500, 2000, 2, 30, True) == False  # credit_score = 500
    assert compute_loan_eligibility(5000, 750, 3000, 2, 30, True) == True  # credit_score = 750
    assert compute_loan_eligibility(5000, 650, 2500, 1, 30, True) == False  # employment_years = 1, credit_score = 650
    assert compute_loan_eligibility(5000, 600, 1000, 2, 30, True) == True  # employment_years = 2, credit_score = 600

    # Edge cases
    assert compute_loan_eligibility(5000, 700, 3000, 0, 30, True) == False  # employment_years = 0
    assert compute_loan_eligibility(5000, 700, 3000, 3, 30, False) == True  # employment_years = 3, no collateral
    assert compute_loan_eligibility(5000, 600, 1000, 3, 30, True) == True  # employment_years = 3, credit_score = 600
    assert compute_loan_eligibility(5000, 600, 2000, 2, 30, False) == False  # employment_years = 2, credit_score = 600, no collateral
    assert compute_loan_eligibility(5000, 700, 3000, 2, 17, True) == False  # age < 18
    assert compute_loan_eligibility(5000, 700, 3000, 2, 71, True) == False  # age > 70