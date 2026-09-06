import inspect

import validkit

ALL_NAMES = [
    "is_valid_email",
    "luhn_check",
    "is_valid_iban",
    "is_valid_isbn13",
    "normalize_phone",
    "strip_accents",
    "mask_secret",
    "slugify",
    "clamp",
]

EXPECTED_SIGNATURES = {
    "is_valid_email": (["text"], ["str"], "bool", {}),
    "luhn_check": (["digits"], ["str | int"], "bool", {}),
    "is_valid_iban": (["text"], ["str"], "bool", {}),
    "is_valid_isbn13": (["text"], ["str"], "bool", {}),
    "normalize_phone": (["text", "country_code"], ["str", "str"], "str", {}),
    "strip_accents": (["text"], ["str"], "str", {}),
    "mask_secret": (["text", "keep"], ["str", "int"], "str", {"keep": 4}),
    "slugify": (["text"], ["str"], "str", {}),
    "clamp": (
        ["value", "low", "high"],
        ["float | int", "float | int", "float | int"],
        "float | int",
        {},
    ),
}


def test_package_is_importable():
    assert validkit.__name__ == "validkit"


def test_all_nine_names_exported():
    assert set(validkit.__all__) == set(ALL_NAMES)
    for name in ALL_NAMES:
        assert callable(getattr(validkit, name))


def test_signatures_match_contract():
    for name in ALL_NAMES:
        params, annotations, return_annotation, defaults = EXPECTED_SIGNATURES[name]
        sig = inspect.signature(getattr(validkit, name))
        assert list(sig.parameters) == params, name
        for pname, expected_annotation in zip(params, annotations, strict=True):
            param = sig.parameters[pname]
            assert param.annotation == expected_annotation, (name, pname)
            if pname in defaults:
                assert param.default == defaults[pname], (name, pname)
            else:
                assert param.default is inspect.Parameter.empty, (name, pname)
        assert sig.return_annotation == return_annotation, name
