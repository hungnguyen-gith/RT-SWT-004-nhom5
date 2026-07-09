import pytest

def test_validate_form_submission_required_fields():
    fields = {"name": "John", "email": "john@example.com"}
    required_fields = ["name", "email", "age"]
    max_lengths = {}
    custom_validators = {}
    assert validate_form_submission(fields, required_fields, max_lengths, custom_validators) == ["age is required"]

def test_validate_form_submission_missing_field():
    fields = {"name": "", "email": "john@example.com"}
    required_fields = ["name", "email"]
    max_lengths = {}
    custom_validators = {}
    assert validate_form_submission(fields, required_fields, max_lengths, custom_validators) == ["name is required"]

def test_validate_form_submission_exceeds_max_length():
    fields = {"username": "a" * 11}
    required_fields = []
    max_lengths = {"username": 10}
    custom_validators = {}
    assert validate_form_submission(fields, required_fields, max_lengths, custom_validators) == ["username exceeds max length"]

def test_validate_form_submission_custom_validator_fail():
    fields = {"password": "123"}
    required_fields = []
    max_lengths = {}
    custom_validators = {"password": lambda x: len(x) > 5}
    assert validate_form_submission(fields, required_fields, max_lengths, custom_validators) == ["password failed validation"]

def test_validate_form_submission_invalid_email_format():
    fields = {"email": "johnexample.com"}
    required_fields = ["email"]
    max_lengths = {}
    custom_validators = {}
    assert validate_form_submission(fields, required_fields, max_lengths, custom_validators) == ["invalid email"]

def test_validate_form_submission_multiple_at_symbols_in_email():
    fields = {"email": "john@@example.com"}
    required_fields = ["email"]
    max_lengths = {}
    custom_validators = {}
    assert validate_form_submission(fields, required_fields, max_lengths, custom_validators) == ["invalid email"]

def test_validate_form_submission_no_errors():
    fields = {"name": "John", "email": "john@example.com", "username": "john_doe"}
    required_fields = ["name", "email"]
    max_lengths = {"username": 10}
    custom_validators = {}
    assert validate_form_submission(fields, required_fields, max_lengths, custom_validators) == []

def test_validate_form_submission_multiple_errors():
    fields = {"name": "", "email": "johnexample.com", "username": "a" * 11}
    required_fields = ["name", "email"]
    max_lengths = {"username": 10}
    custom_validators = {}
    assert validate_form_submission(fields, required_fields, max_lengths, custom_validators) == [
        "name is required", "invalid email", "username exceeds max length"
    ]