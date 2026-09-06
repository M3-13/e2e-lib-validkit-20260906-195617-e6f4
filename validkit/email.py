from __future__ import annotations

import re

_EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def is_valid_email(text: str) -> bool:
    """Return True if ``text`` is a syntactically valid email address.

    Returns False for addresses with missing parts (e.g. ``test@``) rather than
    raising.
    """
    if not isinstance(text, str):
        raise TypeError("is_valid_email expects a str argument")
    return _EMAIL_RE.fullmatch(text) is not None
