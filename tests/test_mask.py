import pytest

from validkit.mask import mask_secret


def test_mask_secret_keeps_last_four_chars():
    assert mask_secret("geheimnisvoll", 4) == "*********voll"


def test_mask_secret_default_keep_is_four():
    assert mask_secret("geheimnisvoll") == "*********voll"


def test_mask_secret_text_shorter_than_keep_fully_masked():
    assert mask_secret("kurz", 4) == "****"


def test_mask_secret_text_equal_length_keep_fully_masked():
    assert mask_secret("voll", 4) == "****"


def test_mask_secret_keep_zero_masks_everything():
    assert mask_secret("geheimnisvoll", 0) == "*************"


def test_mask_secret_keep_greater_than_length_masks_everything():
    assert mask_secret("abc", 10) == "***"


def test_mask_secret_empty_text():
    assert mask_secret("") == ""


def test_mask_secret_negative_keep_raises_value_error():
    with pytest.raises(ValueError):
        mask_secret("x", -1)


def test_mask_secret_non_string_raises_type_error():
    with pytest.raises(TypeError):
        mask_secret(12345)


def test_mask_secret_non_integer_keep_raises_value_error():
    with pytest.raises(ValueError):
        mask_secret("abc", 1.5)
