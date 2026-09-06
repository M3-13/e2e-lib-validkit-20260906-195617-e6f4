import pytest

from validkit.iban import is_valid_iban


def test_valid_german_iban_returns_true():
    assert is_valid_iban("DE89370400440532013000") is True


def test_valid_foreign_iban_returns_true():
    assert is_valid_iban("GB82WEST12345698765432") is True


def test_valid_senegal_iban_returns_true():
    assert is_valid_iban("SN53AB1234567890123456789012") is True


def test_valid_cameroon_iban_returns_true():
    assert is_valid_iban("CM54AB123456789012345678901") is True


def test_wrong_checksum_returns_false():
    assert is_valid_iban("DE89370400440532013001") is False


def test_spaces_are_accepted():
    assert is_valid_iban("DE89 3704 0044 0532 0130 00") is True


def test_lowercase_is_accepted():
    assert is_valid_iban("de89370400440532013000") is True


def test_wrong_length_returns_false():
    assert is_valid_iban("DE8937040044053201300") is False
    assert is_valid_iban("DE893704004405320130000") is False


def test_invalid_country_code_returns_false():
    assert is_valid_iban("XX89370400440532013000") is False


def test_non_str_raises_type_error():
    with pytest.raises(TypeError):
        is_valid_iban(123)
    with pytest.raises(TypeError):
        is_valid_iban(None)
    with pytest.raises(TypeError):
        is_valid_iban(["DE89370400440532013000"])


def test_type_error_message_does_not_leak_input():
    with pytest.raises(TypeError) as exc_info:
        is_valid_iban(123)
    assert "123" not in str(exc_info.value)
