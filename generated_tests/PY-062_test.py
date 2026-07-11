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
        {'name': '', 'email': 'john@example.com'},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {}
    ) == ['name is required']

    assert validate_form_submission(
        {'name': 'John', 'email': 'invalidemail'},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {}
    ) == ['invalid email']

    # Boundary test cases
    assert validate_form_submission(
        {'name': 'A' * 50, 'email': 'john@example.com'},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {}
    ) == []

    assert validate_form_submission(
        {'name': 'A' * 51, 'email': 'john@example.com'},
        ['name', 'email'],
        {'name': 50, 'email': 100},
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
        {'name': 'John', 'email': ''},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {}
    ) == ['email is required']

    assert validate_form_submission(
        {'name': 'John', 'email': 'john@@example.com'},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {}
    ) == ['invalid email']

    assert validate_form_submission(
        {'name': 'John', 'email': 'john@example.com'},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {'name': lambda x: x.isalpha()}
    ) == []

    assert validate_form_submission(
        {'name': 'John123', 'email': 'john@example.com'},
        ['name', 'email'],
        {'name': 50, 'email': 100},
        {'name': lambda x: x.isalpha()}
    ) == ['name failed validation']