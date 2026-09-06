from __future__ import annotations

import pytest

from validkit.slug import slugify


def test_slugify_normal_case():
    assert slugify("Héllo, Wörld!") == "hello-world"


def test_slugify_empty_string():
    assert slugify("") == ""


def test_slugify_only_special_characters():
    assert slugify("!!!") == ""


def test_slugify_collapses_repeated_hyphens():
    assert slugify("a--b  c") == "a-b-c"


def test_slugify_strips_leading_and_trailing_hyphens():
    assert slugify("-hello world-") == "hello-world"


def test_slugify_non_str_raises_type_error():
    with pytest.raises(TypeError):
        slugify(123)
