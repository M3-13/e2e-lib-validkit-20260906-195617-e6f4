import pytest

from validkit.phone import normalize_phone


def test_normal_case_de():
    assert normalize_phone("030 1234567", "DE") == "+49301234567"


def test_leading_zeros_removed():
    assert normalize_phone("0030 1234567", "DE") == "+49301234567"


def test_numeric_country_code_with_plus_accepted():
    assert normalize_phone("030 1234567", "+49") == "+49301234567"


def test_numeric_country_code_without_plus_accepted():
    assert normalize_phone("030 1234567", "49") == "+49301234567"


def test_iso_code_case_insensitive():
    assert normalize_phone("123 4567", "at") == "+431234567"


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("DE", "49"),
        ("AT", "43"),
        ("CH", "41"),
        ("US", "1"),
        ("GB", "44"),
        ("FR", "33"),
        ("IT", "39"),
        ("ES", "34"),
        ("NL", "31"),
    ],
)
def test_iso_code_mapping(code, expected):
    assert normalize_phone("1234567", code) == "+" + expected + "1234567"


def test_separators_are_stripped():
    assert normalize_phone("(030) 123-45/67.", "DE") == "+49301234567"


def test_non_digit_remainder_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("030-12x", "DE")


def test_non_digit_remainder_message_does_not_leak_input():
    with pytest.raises(ValueError) as exc_info:
        normalize_phone("030-12x", "DE")
    message = str(exc_info.value)
    assert "030-12x" not in message
    assert "12x" not in message


def test_empty_text_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("", "DE")


def test_only_zeros_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("000", "DE")


def test_unknown_country_code_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("030 1234567", "XX")


def test_empty_country_code_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("030 1234567", "")


def test_non_string_text_raises_type_error():
    with pytest.raises(TypeError):
        normalize_phone(301234567, "DE")


def test_non_string_country_code_raises_type_error():
    with pytest.raises(TypeError):
        normalize_phone("030 1234567", 49)


def test_type_error_message_does_not_leak_input():
    with pytest.raises(TypeError) as exc_info:
        normalize_phone("030 1234567", 49)
    assert "030 1234567" not in str(exc_info.value)
