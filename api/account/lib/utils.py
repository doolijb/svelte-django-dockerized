from django.contrib.auth.password_validation import validate_password as base_validate_password


def is_hashed(string: str) -> bool:
    """
    Return whether a string is likely encrypted.
    """
    return (
        (
            string.startswith("$2b$")
            or string.startswith("$2y$")
            or string.startswith("$2a$")
            or string.startswith("$2x$")
            or string.startswith("$2$")
            or string.startswith("$argon$")
            or string.startswith("$scrypt$")
            or string.startswith("$pbkdf2$")
            or string.startswith("$sha$")
            or string.startswith("$bcrypt$")
            or string.startswith("$scrypt$")
        ) and len(string) >= 60
    )


def normalize_email(email):
        """
        Normalize the email address by lowercasing the domain part of the email
        """
        return email.lower().strip()


def validate_password(raw_password: str) -> None:
        """
            Validates a password and raises a ValidationError if it's invalid.
        """
        # TODO: Add validators
        assert not is_hashed(raw_password), "Raw password must not be already hashed"
        return base_validate_password(raw_password)
