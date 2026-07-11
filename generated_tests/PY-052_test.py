import pytest

def test_validate_password():
    # Normal test cases
    assert validate_password("Password1") == True
    assert validate_password("Password!") == True
    assert validate_password("password1") == False
    assert validate_password("PASSWORD1") == False
    assert validate_password("Pass1") == False
    assert validate_password("Pass!1") == True

    # Boundary test cases
    assert validate_password("Pass1234") == True
    assert validate_password("Pass123") == False
    assert validate_password("12345678") == False
    assert validate_password("abcdefgh") == False
    assert validate_password("ABCDEFGH") == False
    assert validate_password("!@#$%^&*") == False

    # Edge cases
    assert validate_password("") == False
    assert validate_password("1234567") == False
    assert validate_password("abcdefgh", require_digit=False, require_upper=False) == True
    assert validate_password("ABCDEFGH", require_digit=False, require_special=True) == False
    assert validate_password("Password", require_special=True) == False
    assert validate_password("Password1!", require_special=True) == True
    assert validate_password("P@ssw0rd", require_special=True) == True