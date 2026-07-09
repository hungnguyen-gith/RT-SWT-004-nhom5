import pytest

def test_valid_password():
    assert validate_password("Valid1Password!", 8, True, True, True) == True

def test_too_short_password():
    assert validate_password("Short1!", 8, True, True, True) == False

def test_missing_digit():
    assert validate_password("MissingDigit!", 8, True, True, True) == False

def test_missing_uppercase():
    assert validate_password("missingdigit1!", 8, True, True, True) == False

def test_missing_special_character():
    assert validate_password("MissingSpecial1", 8, True, True, True) == False

def test_valid_password_without_special():
    assert validate_password("Valid1Password", 8, True, True, False) == True

def test_valid_password_without_digit():
    assert validate_password("ValidPassword!", 8, False, True, True) == True

def test_valid_password_without_upper():
    assert validate_password("validpassword1", 8, True, False, True) == True

def test_valid_password_without_digit_and_upper():
    assert validate_password("validpassword!", 8, False, False, True) == True

def test_valid_password_with_min_length():
    assert validate_password("12345678", 8, True, True, False) == False

def test_valid_password_with_custom_min_length():
    assert validate_password("12345678", 10, True, True, False) == False

def test_valid_password_with_special_required():
    assert validate_password("Valid1Password", 8, True, True, True) == False

def test_valid_password_with_special_character():
    assert validate_password("Valid1Password@", 8, True, True, True) == True

def test_empty_password():
    assert validate_password("", 8, True, True, True) == False

def test_password_with_only_special_characters():
    assert validate_password("!@#$%^&*", 8, True, True, True) == False

def test_password_with_only_digits():
    assert validate_password("12345678", 8, True, True, True) == False

def test_password_with_only_uppercase():
    assert validate_password("ABCDEFGH", 8, True, True, True) == False

def test_password_with_only_lowercase():
    assert validate_password("abcdefgh", 8, True, True, True) == False