from __future__ import annotations

_DIAL_CODE_BY_COUNTRY: dict[str, str] = {
    "DE": "49",
    "AT": "43",
    "CH": "41",
    "US": "1",
    "GB": "44",
    "FR": "33",
    "IT": "39",
    "ES": "34",
    "NL": "31",
}

_SEPARATORS = frozenset(" \t\r\n-()./")


def _resolve_dial_code(country_code: str) -> str:
    """Return the dial code (without leading ``+``) for ``country_code``.

    Accepts a numeric code with or without a leading ``+`` (``"49"``, ``"+49"``)
    as well as an ISO-3166-1 alpha-2 code (``"DE"``, ``"de"``). Raises ValueError
    for anything unknown.
    """
    candidate = country_code.strip()
    if candidate.startswith("+"):
        candidate = candidate[1:]
    if not candidate:
        raise ValueError("unknown country code")
    if candidate.isdigit():
        return candidate
    code = _DIAL_CODE_BY_COUNTRY.get(candidate.upper())
    if code is None:
        raise ValueError("unknown country code")
    return code


def _extract_national_digits(text: str) -> str:
    """Return the national digits of ``text`` with leading zeros stripped.

    Formatting separators (spaces, hyphens, dots, parentheses, slashes) are
    ignored; any other non-digit character raises ValueError, as does a text
    that yields no digits at all.
    """
    digits: list[str] = []
    for char in text:
        if "0" <= char <= "9":
            digits.append(char)
        elif char not in _SEPARATORS:
            raise ValueError("invalid character in phone number")
    national = "".join(digits).lstrip("0")
    if not national:
        raise ValueError("phone number contains no digits")
    return national


def normalize_phone(text: str, country_code: str) -> str:
    """Normalize ``text`` to an E.164 phone number using ``country_code``."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(country_code, str):
        raise TypeError("country_code must be a string")

    dial_code = _resolve_dial_code(country_code)
    national = _extract_national_digits(text)
    return "+" + dial_code + national
