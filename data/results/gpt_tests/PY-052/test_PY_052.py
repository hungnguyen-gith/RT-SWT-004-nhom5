import pytest

def test_validate_password():
    # Normal test cases
    assert validate_password("Password1") == True
    assert validate_password("Password!") == True
    assert validate_password("Pass1!") == True
    assert validate_password("password1") == False  # No uppercase
    assert validate_password("PASSWORD1") == False  # No lowercase
    assert validate_password("Password") == False  # No digit
    assert validate_password("Password1!") == True  # All requirements met

    # Boundary test cases
    assert validate_password("Pass1") == False  # Below min_length
    assert validate_password("Pass1234") == True  # Exactly min_length with digit and upper
    assert validate_password("12345678") == False  # No upper and special
    assert validate_password("ABCDEFGH") == False  # No digit and special
    assert validate_password("!@#$%^&*") == False  # No digit and upper

    # Edge cases
    assert validate_password("P@ssw0rd") == True  # All requirements met
    assert validate_password("P@ssw0rd", min_length=10) == False  # Min length not met
    assert validate_password("P@ssw0rd", require_special=True) == True  # Special required, met
    assert validate_password("Password1", require_special=True) == False  # Special required, not met
    assert validate_password("", min_length=1) == False  # Empty password, below min_length
    assert validate_password("A1!", min_length=3, require_special=True) == True  # Special required, met