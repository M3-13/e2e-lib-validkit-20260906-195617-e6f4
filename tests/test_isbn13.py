from __future__ import annotations

import pytest

from validkit.isbn13 import is_valid_isbn13


def test_valid_isbn13_with_separators():
    assert is_valid_isbn13("978-3-16-148410-0") is True


def test_valid_isbn13_without_separators():
    assert is_valid_isbn13("9783161484100") is True


def test_valid_isbn13_with_spaces():
    assert is_valid_isbn13("978 3 16 148410 0") is True


def test_valid_isbn13_prefix_979():
    assert is_valid_isbn13("979-0-00-000000-1") is True


def test_wrong_check_digit():
    assert is_valid_isbn13("978-3-16-148410-1") is False


def test_wrong_prefix():
    assert is_valid_isbn13("977-3-16-148410-0") is False


def test_too_short():
    assert is_valid_isbn13("978-3-16-14841") is False


def test_too_long():
    assert is_valid_isbn13("978-3-16-148410-00") is False


def test_non_digit_character():
    assert is_valid_isbn13("978-3-16-14841X-0") is False


def test_non_str_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_isbn13(9783161484100)  # type: ignore[arg-type]


def test_type_error_message_does_not_leak_input():
    with pytest.raises(TypeError) as excinfo:
        is_valid_isbn13(12345)  # type: ignore[arg-type]
    assert "12345" not in str(excinfo.value)
