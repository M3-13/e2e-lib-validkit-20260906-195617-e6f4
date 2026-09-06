import pytest

from validkit.accents import strip_accents


def test_strip_accents_normal():
    assert strip_accents("Müller café") == "Muller cafe"


def test_strip_accents_plain_text_unchanged():
    assert strip_accents("Hello world") == "Hello world"


def test_strip_accents_empty_string():
    assert strip_accents("") == ""


def test_strip_accents_keeps_non_letter_characters():
    assert strip_accents("Ångström 123!") == "Angstrom 123!"


def test_strip_accents_non_str_raises_type_error():
    with pytest.raises(TypeError):
        strip_accents(123)
