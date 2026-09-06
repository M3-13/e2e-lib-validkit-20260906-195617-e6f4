from __future__ import annotations


def mask_secret(text: str, keep: int = 4) -> str:
    """Mask ``text``, keeping only the last ``keep`` characters visible.

    Raises ``TypeError`` if ``text`` is not a ``str`` and ``ValueError`` if
    ``keep`` is not a non-negative integer.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if isinstance(keep, bool) or not isinstance(keep, int) or keep < 0:
        raise ValueError("keep must be a non-negative integer")

    if len(text) <= keep or keep == 0:
        return "*" * len(text)
    return "*" * (len(text) - keep) + text[-keep:]
