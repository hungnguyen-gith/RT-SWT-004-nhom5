import pytest

from your_module import compute_loan_eligibility

def test_age_below_18():
    assert compute_loan_eligibility(50000, 600, 10000, 2, 17, True) == False

def test_age_above_70():
    assert compute_loan_eligibility(50000, 600, 10000, 2, 71, True) == False

def test_credit_score_below_500():
    assert compute_loan_eligibility(50000, 400, 10000, 2, 30, True) == False

def test_debt_ratio_above_0_5_no_collateral():
    assert compute_loan_eligibility(50000, 600, 30000, 2, 30, False) == False

def test_debt_ratio_above_0_5_below_650():
    assert compute_loan_eligibility(50000, 600, 30000, 2, 30, True) == False

def test_employment_years_below_1_below_700():
    assert compute_loan_eligibility(50000, 650, 10000, 0, 30, True) == False

def test_employment_years_below_3_below_600():
    assert compute_loan_eligibility(50000, 550, 10000, 2, 30, True) == False

def test_credit_score_750_or_above():
    assert compute_loan_eligibility(50000, 750, 10000, 2, 30, True) == True

def test_credit_score_650_or_above_with_debt_ratio_0_4_or_below():
    assert compute_loan_eligibility(50000, 650, 20000, 2, 30, True) == True

def test_credit_score_650_or_above_with_debt_ratio_above_0_4():
    assert compute_loan_eligibility(50000, 650, 25000, 2, 30, True) == False

def test_credit_score_below_650_with_debt_ratio_0_2_or_below_and_collateral():
    assert compute_loan_eligibility(50000, 600, 5000, 2, 30, True) == True

def test_credit_score_below_650_with_debt_ratio_above_0_2_or_no_collateral():
    assert compute_loan_eligibility(50000, 600, 15000, 2, 30, False) == False