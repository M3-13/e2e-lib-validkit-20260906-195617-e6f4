import pytest

from validkit.clamp import clamp


def test_within_range_returns_value_unchanged():
    assert clamp(5, 0, 10) == 5


def test_below_range_clamps_to_low():
    assert clamp(-5, 0, 10) == 0


def test_above_range_clamps_to_high():
    assert clamp(15, 0, 10) == 10


def test_value_equal_to_low_is_unchanged():
    assert clamp(0, 0, 10) == 0


def test_value_equal_to_high_is_unchanged():
    assert clamp(10, 0, 10) == 10


def test_float_values():
    assert clamp(5.5, 0.0, 10.0) == 5.5
    assert clamp(-1.5, 0.0, 10.0) == 0.0
    assert clamp(11.5, 0.0, 10.0) == 10.0


def test_int_input_returns_int():
    result = clamp(15, 0, 10)
    assert result == 10
    assert isinstance(result, int)


def test_float_input_returns_float():
    result = clamp(15.0, 0.0, 10.0)
    assert result == 10.0
    assert isinstance(result, float)


def test_low_greater_than_high_raises_value_error():
    with pytest.raises(ValueError):
        clamp(1, 10, 0)


def test_non_numeric_value_raises_type_error():
    with pytest.raises(TypeError):
        clamp("a", 0, 10)


def test_non_numeric_low_raises_type_error():
    with pytest.raises(TypeError):
        clamp(0, "a", 10)


def test_non_numeric_high_raises_type_error():
    with pytest.raises(TypeError):
        clamp(0, 0, "a")


def test_boolean_input_is_rejected():
    with pytest.raises(TypeError):
        clamp(True, 0, 10)


def test_type_error_message_does_not_leak_input():
    with pytest.raises(TypeError) as exc_info:
        clamp("secret", 0, 10)
    assert "secret" not in str(exc_info.value)


def test_value_error_message_does_not_leak_input():
    with pytest.raises(ValueError) as exc_info:
        clamp(5, 10, 0)
    assert "5" not in str(exc_info.value)
