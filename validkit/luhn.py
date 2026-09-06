from __future__ import annotations


def luhn_check(digits: str | int) -> bool:
    """Return True if ``digits`` satisfies the Luhn checksum algorithm.

    Starting from the rightmost digit, every second digit is doubled; if
    doubling produces a value greater than 9 its digit sum is used instead
    (i.e. 9 is subtracted). The number is valid when the total of all
    processed digits is a multiple of 10.

    Args:
        digits: A string of digits or a non-negative integer.

    Returns:
        True if the checksum is valid, False otherwise. A single digit
        always yields False.

    Raises:
        TypeError: If ``digits`` is neither a ``str`` nor an ``int``.
        ValueError: If ``digits`` is an empty string, a ``str`` containing
            non-digit characters, or a negative ``int``.
    """
    if isinstance(digits, bool) or not isinstance(digits, (str, int)):
        raise TypeError("digits must be a str or int")

    if isinstance(digits, str):
        if not digits:
            raise ValueError("digits must not be empty")
        if not digits.isdigit():
            raise ValueError("digits must contain only digit characters")
    else:
        if digits < 0:
            raise ValueError("digits must not be negative")
        digits = str(digits)

    if len(digits) < 2:
        return False

    total = 0
    for index, char in enumerate(reversed(digits)):
        digit = int(char)
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0
