from functions.PY_052 import validate_password

def test_valid_password():
    assert validate_password("Valid1Password", min_length=8, require_digit=True, require_upper=True, require_special=False) is True

def test_valid_password_with_special():
    assert validate_password("Valid1Password!", min_length=8, require_digit=True, require_upper=True, require_special=True) is True

def test_too_short_password():
    assert validate_password("Short1", min_length=8) is False

def test_missing_digit():
    assert validate_password("MissingDigitPassword", min_length=8, require_digit=True) is False

def test_missing_uppercase():
    assert validate_password("missingdigit1", min_length=8, require_upper=True) is False

def test_missing_special_character():
    assert validate_password("Valid1Password", min_length=8, require_special=True) is False

def test_valid_password_without_requirements():
    assert validate_password("password", min_length=8, require_digit=False, require_upper=False, require_special=False) is True

def test_valid_password_with_only_digit_requirement():
    assert validate_password("12345678", min_length=8, require_digit=True, require_upper=False, require_special=False) is True

def test_valid_password_with_only_uppercase_requirement():
    assert validate_password("UPPERCASE", min_length=8, require_digit=False, require_upper=True, require_special=False) is True

def test_valid_password_with_only_special_requirement():
    assert validate_password("!@#$%^&*", min_length=8, require_digit=False, require_upper=False, require_special=True) is True

def test_invalid_password_with_all_requirements():
    assert validate_password("abc", min_length=8, require_digit=True, require_upper=True, require_special=True) is False

def test_edge_case_empty_password():
    assert validate_password("", min_length=8) is False

def test_edge_case_exact_length_with_requirements():
    assert validate_password("A1!valid", min_length=8, require_digit=True, require_upper=True, require_special=True) is True

def test_edge_case_exact_length_without_special():
    assert validate_password("A1valid", min_length=8, require_digit=True, require_upper=True, require_special=False) is True

def test_edge_case_exact_length_without_digit():
    assert validate_password("Avalid!", min_length=8, require_digit=True, require_upper=True, require_special=True) is False

def test_edge_case_exact_length_without_upper():
    assert validate_password("1valid!", min_length=8, require_digit=True, require_upper=True, require_special=True) is False