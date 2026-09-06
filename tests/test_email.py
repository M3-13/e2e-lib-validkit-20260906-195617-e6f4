import re

import pytest

import validkit.email


def _has_nested_quantifier(pattern: str) -> bool:
    """Return True if ``pattern`` quantifies a group that already contains a quantifier."""
    return bool(re.search(r"\((?:[^()]|\\.)*[+*?](?:[^()]|\\.)*\)\s*[+*?{]", pattern))


def test_valid_email():
    assert validkit.email.is_valid_email("test@example.com") is True


def test_domain_without_dot_is_invalid():
    assert validkit.email.is_valid_email("test@example") is False


def test_missing_domain_is_invalid():
    assert validkit.email.is_valid_email("test@") is False


def test_missing_at_is_invalid():
    assert validkit.email.is_valid_email("testexample.com") is False


def test_non_string_raises_type_error():
    with pytest.raises(TypeError):
        validkit.email.is_valid_email(123)


def test_type_error_message_does_not_leak_input():
    with pytest.raises(TypeError) as excinfo:
        validkit.email.is_valid_email(123)
    assert "123" not in str(excinfo.value)


def test_regex_has_no_nested_quantifier():
    assert not _has_nested_quantifier(validkit.email._EMAIL_RE.pattern)
