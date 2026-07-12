from functions.PY_063 import compute_tax_bracket

def test_compute_tax_bracket_single_no_dependents():
    assert compute_tax_bracket(50000, "single", 10000, 0, False) == 6750.0

def test_compute_tax_bracket_single_with_dependents():
    assert compute_tax_bracket(50000, "single", 10000, 2, False) == 5750.0

def test_compute_tax_bracket_single_senior():
    assert compute_tax_bracket(50000, "single", 10000, 0, True) == 6412.5

def test_compute_tax_bracket_single_senior_with_dependents():
    assert compute_tax_bracket(50000, "single", 10000, 2, True) == 5431.25

def test_compute_tax_bracket_married_no_dependents():
    assert compute_tax_bracket(50000, "married", 10000, 0, False) == 6750.0

def test_compute_tax_bracket_married_with_dependents():
    assert compute_tax_bracket(50000, "married", 10000, 2, False) == 5750.0

def test_compute_tax_bracket_married_senior():
    assert compute_tax_bracket(50000, "married", 10000, 0, True) == 6412.5

def test_compute_tax_bracket_married_senior_with_dependents():
    assert compute_tax_bracket(50000, "married", 10000, 2, True) == 5431.25

def test_compute_tax_bracket_zero_income():
    assert compute_tax_bracket(0, "single", 0, 0, False) == 0.0

def test_compute_tax_bracket_negative_income():
    assert compute_tax_bracket(-10000, "single", 0, 0, False) == 0.0

def test_compute_tax_bracket_no_deductions():
    assert compute_tax_bracket(30000, "single", 0, 0, False) == 3750.0

def test_compute_tax_bracket_invalid_filing_status():
    assert compute_tax_bracket(50000, "invalid", 10000, 0, False) == 8000.0

def test_compute_tax_bracket_high_income():
    assert compute_tax_bracket(200000, "single", 50000, 0, False) == 52500.0

def test_compute_tax_bracket_high_income_married():
    assert compute_tax_bracket(200000, "married", 50000, 0, False) == 52500.0

def test_compute_tax_bracket_edge_case_single():
    assert compute_tax_bracket(10000, "single", 0, 0, False) == 1000.0

def test_compute_tax_bracket_edge_case_married():
    assert compute_tax_bracket(20000, "married", 0, 0, False) == 2000.0

def test_compute_tax_bracket_senior_no_tax():
    assert compute_tax_bracket(1000, "single", 0, 0, True) == 0.0

def test_compute_tax_bracket_senior_with_dependents_no_tax():
    assert compute_tax_bracket(1000, "single", 0, 1, True) == 0.0