import re


def validate_username(username: str) -> None:
    if re.search(r"^[A-Za-z_]*$", username) is None:
        raise ValueError(f"{username} contains non English letters "
                         f"or characters other than underscore")
    if username.startswith("_") or username.endswith("_"):
        raise ValueError(f"{username} cannot start or end with an underscore")


def validate_email(email: str) -> None:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.search(pattern, email):
        raise ValueError("Invalid email format")


def validate_password_strength(password: str) -> None:
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")
    if not re.search(r'[A-Z]', password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValueError("Password must contain at least one lower letter.")
    if not re.search(r'\d', password):
        raise ValueError("Password must contain at least one digit.")
    if not re.search(r'[@$!%*?&#]', password):
        raise ValueError("Password must contain at least "
                         "one special character: @, $, !, %, *, ?, #, &.")
