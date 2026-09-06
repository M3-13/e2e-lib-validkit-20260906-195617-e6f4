from __future__ import annotations

import unicodedata


def slugify(text: str) -> str:
    """Return a URL-safe slug for ``text`` (e.g. ``Héllo, Wörld!`` -> ``hello-world``)."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    decomposed = unicodedata.normalize("NFD", text)
    without_accents = "".join(char for char in decomposed if not unicodedata.combining(char))

    slug = "".join(char if char.isalnum() else "-" for char in without_accents.lower())
    return "-".join(part for part in slug.split("-") if part)
