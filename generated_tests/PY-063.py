import pytest

def test_compute_tax_bracket_single_no_dependents():
    assert compute_tax_bracket(50000, "single", 10000, 0, False) == 6750.0

def test_compute_tax_bracket_single_with_dependents():
    assert compute_tax_bracket(50000, "single", 10000, 2, False) == 5750.0

def test_compute_tax_bracket_single_senior_no_dependents():
    assert compute_tax_bracket(50000, "single", 10000, 0, True) == 6412.5

def test_compute_tax_bracket_single_senior_with_dependents():
    assert compute_tax_bracket(50000, "single", 10000, 2, True) == 5431.25

def test_compute_tax_bracket_married_no_dependents():
    assert compute_tax_bracket(50000, "married", 10000, 0, False) == 6750.0

def test_compute_tax_bracket_married_with_dependents():
    assert compute_tax_bracket(50000, "married", 10000, 2, False) == 5750.0

def test_compute_tax_bracket_married_senior_no_dependents():
    assert compute_tax_bracket(50000, "married", 10000, 0, True) == 6412.5

def test_compute_tax_bracket_married_senior_with_dependents():
    assert compute_tax_bracket(50000, "married", 10000, 2, True) == 5431.25

def test_compute_tax_bracket_other_filing_status():
    assert compute_tax_bracket(50000, "other", 10000, 0, False) == 10000.0

def test_compute_tax_bracket_negative_taxable_income():
    assert compute_tax_bracket(15000, "single", 20000, 0, False) == 0.0

def test_compute_tax_bracket_zero_income():
    assert compute_tax_bracket(0, "single", 0, 0, False) == 0.0

def test_compute_tax_bracket_high_income():
    assert compute_tax_bracket(200000, "single", 50000, 0, False) == 52500.0

def test_compute_tax_bracket_high_income_senior():
    assert compute_tax_bracket(200000, "single", 50000, 0, True) == 49875.0