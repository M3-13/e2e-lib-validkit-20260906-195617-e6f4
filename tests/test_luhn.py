import pytest

from validkit.luhn import luhn_check


def test_valid_checksum_returns_true():
    assert luhn_check("79927398713") is True


def test_valid_checksum_as_int_returns_true():
    assert luhn_check(79927398713) is True


def test_invalid_checksum_returns_false():
    assert luhn_check("79927398712") is False


def test_single_digit_returns_false():
    assert luhn_check("5") is False


def test_non_digit_string_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("abc")


def test_empty_string_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("")


def test_negative_int_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check(-123)


def test_wrong_type_raises_type_error():
    with pytest.raises(TypeError):
        luhn_check(12.5)


def test_bool_raises_type_error():
    with pytest.raises(TypeError):
        luhn_check(True)
