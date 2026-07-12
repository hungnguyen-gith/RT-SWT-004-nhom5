from functions.PY_062 import validate_form_submission

def test_validate_form_submission_success():
    fields = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword"
    }
    required_fields = ["username", "email", "password"]
    max_lengths = {
        "username": 20,
        "password": 20
    }
    custom_validators = {}

    errors = validate_form_submission(fields, required_fields, max_lengths, custom_validators)
    assert errors == []

def test_validate_form_submission_missing_required_field():
    fields = {
        "username": "testuser",
        "email": ""
    }
    required_fields = ["username", "email", "password"]
    max_lengths = {
        "username": 20,
        "password": 20
    }
    custom_validators = {}

    errors = validate_form_submission(fields, required_fields, max_lengths, custom_validators)
    assert errors == ["password is required"]

def test_validate_form_submission_exceeds_max_length():
    fields = {
        "username": "thisusernameiswaytoolong",
        "email": "test@example.com",
        "password": "securepassword"
    }
    required_fields = ["username", "email", "password"]
    max_lengths = {
        "username": 20,
        "password": 20
    }
    custom_validators = {}

    errors = validate_form_submission(fields, required_fields, max_lengths, custom_validators)
    assert errors == ["username exceeds max length"]

def test_validate_form_submission_custom_validator_failure():
    def custom_email_validator(email):
        return email.endswith("@example.com")

    fields = {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "securepassword"
    }
    required_fields = ["username", "email", "password"]
    max_lengths = {
        "username": 20,
        "password": 20
    }
    custom_validators = {
        "email": custom_email_validator
    }

    errors = validate_form_submission(fields, required_fields, max_lengths, custom_validators)
    assert errors == ["email failed validation"]

def test_validate_form_submission_invalid_email_format():
    fields = {
        "username": "testuser",
        "email": "invalidemail",
        "password": "securepassword"
    }
    required_fields = ["username", "email", "password"]
    max_lengths = {
        "username": 20,
        "password": 20
    }
    custom_validators = {}

    errors = validate_form_submission(fields, required_fields, max_lengths, custom_validators)
    assert errors == ["invalid email"]

def test_validate_form_submission_multiple_at_symbols_in_email():
    fields = {
        "username": "testuser",
        "email": "test@@example.com",
        "password": "securepassword"
    }
    required_fields = ["username", "email", "password"]
    max_lengths = {
        "username": 20,
        "password": 20
    }
    custom_validators = {}

    errors = validate_form_submission(fields, required_fields, max_lengths, custom_validators)
    assert errors == ["invalid email"]

def test_validate_form_submission_empty_fields():
    fields = {}
    required_fields = ["username", "email", "password"]
    max_lengths = {
        "username": 20,
        "password": 20
    }
    custom_validators = {}

    errors = validate_form_submission(fields, required_fields, max_lengths, custom_validators)
    assert errors == ["username is required", "email is required", "password is required"]