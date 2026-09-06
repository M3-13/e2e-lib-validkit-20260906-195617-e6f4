from __future__ import annotations


def is_valid_isbn13(text: str) -> bool:
    """Return True if ``text`` is a valid ISBN-13 identifier.

    Hyphens and spaces are ignored. The remaining characters must form exactly
    13 digits, begin with the prefix ``978`` or ``979`` and end with a correct
    check digit (alternating weights 1 and 3 over the first 12 digits).
    Raises TypeError for non-str input.
    """
    if not isinstance(text, str):
        raise TypeError("isbn13 must be a string")

    digits = text.replace("-", "").replace(" ", "")
    if len(digits) != 13 or any(ch < "0" or ch > "9" for ch in digits):
        return False
    if not digits.startswith(("978", "979")):
        return False

    total = sum(int(ch) * (1 if index % 2 == 0 else 3) for index, ch in enumerate(digits[:12]))
    check_digit = (10 - (total % 10)) % 10

    return check_digit == int(digits[12])
