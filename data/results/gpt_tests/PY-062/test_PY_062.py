import pytest

def test_validate_form_submission():
    # Normal test cases
    assert validate_form_submission(
        {'name': 'John', 'email': 'john@example.com'},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {}
    ) == []

    assert validate_form_submission(
        {'name': 'John', 'email': 'john@example.com', 'age': '30'},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {}
    ) == []

    # Boundary test cases
    assert validate_form_submission(
        {'name': 'A' * 50, 'email': 'john@example.com'},
        ['name', 'email'],
        {'name': 50},
        {}
    ) == []

    assert validate_form_submission(
        {'name': 'A' * 51, 'email': 'john@example.com'},
        ['name', 'email'],
        {'name': 50},
        {}
    ) == ['name exceeds max length']

    # Edge cases
    assert validate_form_submission(
        {},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {}
    ) == ['name is required', 'email is required']

    assert validate_form_submission(
        {'name': '', 'email': ''},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {}
    ) == ['name is required', 'email is required']

    assert validate_form_submission(
        {'name': 'John', 'email': 'invalid-email'},
        ['name', 'email'],
        {'name': 50},
        {}
    ) == ['invalid email']

    assert validate_form_submission(
        {'name': 'John', 'email': 'john@example.com', 'custom_field': 'value'},
        ['name', 'email'],
        {'name': 50},
        {'custom_field': lambda x: x == 'valid'}
    ) == []

    assert validate_form_submission(
        {'name': 'John', 'email': 'john@example.com', 'custom_field': 'invalid'},
        ['name', 'email'],
        {'name': 50},
        {'custom_field': lambda x: x == 'valid'}
    ) == ['custom_field failed validation']

    assert validate_form_submission(
        {'name': 'John', 'email': 'john@example.com', 'email2': 'john@example.com'},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {}
    ) == []