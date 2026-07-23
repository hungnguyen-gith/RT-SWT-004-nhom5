def validate_password(password, min_length=8, require_digit=True, require_upper=True, require_special=False):

    if len(password) < min_length:

        return False

    has_digit = any(c.isdigit() for c in password)

    has_upper = any(c.isupper() for c in password)

    has_special = any(not c.isalnum() for c in password)

    if require_digit and not has_digit:

        return False

    if require_upper and not has_upper:

        return False

    if require_special and not has_special:

        return False

    return True
