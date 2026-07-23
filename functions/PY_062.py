def validate_form_submission(fields, required_fields, max_lengths, custom_validators):

    errors = []

    for field in required_fields:

        if field not in fields or not fields[field]:

            errors.append(f"{field} is required")

    for field, value in fields.items():

        if field in max_lengths:

            if value and len(value) > max_lengths[field]:

                errors.append(f"{field} exceeds max length")

        if field in custom_validators:

            validator = custom_validators[field]

            if value:

                if not validator(value):

                    errors.append(f"{field} failed validation")

    if "email" in fields and fields["email"]:

        if "@" not in fields["email"]:

            errors.append("invalid email")

        elif fields["email"].count("@") > 1:

            errors.append("invalid email")

    return errors
