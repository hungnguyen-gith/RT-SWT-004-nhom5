from functions.PY_058 import compute_loan_eligibility

def test_loan_eligibility_underage():
    assert compute_loan_eligibility(50000, 600, 10000, 2, 17, True) == False

def test_loan_eligibility_overage():
    assert compute_loan_eligibility(50000, 600, 10000, 2, 71, True) == False

def test_loan_eligibility_low_credit_score():
    assert compute_loan_eligibility(50000, 400, 10000, 2, 30, True) == False

def test_loan_eligibility_zero_income():
    assert compute_loan_eligibility(0, 600, 10000, 2, 30, True) == False

def test_loan_eligibility_high_debt_ratio_no_collateral():
    assert compute_loan_eligibility(50000, 600, 30000, 2, 30, False) == False

def test_loan_eligibility_high_debt_ratio_with_collateral_low_credit():
    assert compute_loan_eligibility(50000, 600, 30000, 2, 30, True) == False

def test_loan_eligibility_high_debt_ratio_with_collateral_high_credit():
    assert compute_loan_eligibility(50000, 700, 30000, 2, 30, True) == False

def test_loan_eligibility_employment_years_less_than_one():
    assert compute_loan_eligibility(50000, 650, 10000, 0, 30, True) == False

def test_loan_eligibility_employment_years_one_high_credit():
    assert compute_loan_eligibility(50000, 700, 10000, 1, 30, True) == True

def test_loan_eligibility_employment_years_one_low_credit():
    assert compute_loan_eligibility(50000, 600, 10000, 1, 30, True) == False

def test_loan_eligibility_employment_years_two_high_credit():
    assert compute_loan_eligibility(50000, 700, 10000, 2, 30, True) == True

def test_loan_eligibility_employment_years_two_low_credit():
    assert compute_loan_eligibility(50000, 600, 10000, 2, 30, True) == False

def test_loan_eligibility_employment_years_three_high_credit():
    assert compute_loan_eligibility(50000, 700, 10000, 3, 30, True) == True

def test_loan_eligibility_employment_years_three_low_credit():
    assert compute_loan_eligibility(50000, 600, 10000, 3, 30, True) == False

def test_loan_eligibility_credit_score_750():
    assert compute_loan_eligibility(50000, 750, 10000, 2, 30, True) == True

def test_loan_eligibility_credit_score_650_with_good_debt_ratio():
    assert compute_loan_eligibility(50000, 650, 15000, 2, 30, True) == True

def test_loan_eligibility_credit_score_650_with_bad_debt_ratio():
    assert compute_loan_eligibility(50000, 650, 25000, 2, 30, True) == False

def test_loan_eligibility_credit_score_600_with_collateral_and_good_debt_ratio():
    assert compute_loan_eligibility(50000, 600, 8000, 2, 30, True) == True

def test_loan_eligibility_credit_score_600_with_collateral_and_bad_debt_ratio():
    assert compute_loan_eligibility(50000, 600, 15000, 2, 30, True) == False

def test_loan_eligibility_credit_score_600_without_collateral_and_good_debt_ratio():
    assert compute_loan_eligibility(50000, 600, 8000, 2, 30, False) == False

def test_loan_eligibility_credit_score_600_without_collateral_and_bad_debt_ratio():
    assert compute_loan_eligibility(50000, 600, 15000, 2, 30, False) == False