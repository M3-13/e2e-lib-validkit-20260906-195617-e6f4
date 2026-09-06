from __future__ import annotations


def clamp(value: float | int, low: float | int, high: float | int) -> float | int:
    """Return ``value`` constrained to the inclusive range ``[low, high]``.

    ``value`` is returned unchanged when ``low <= value <= high``; otherwise it is
    clamped to ``low`` or ``high``. ``bool`` is rejected as it is not a meaningful
    numeric input. The return type matches the type of ``value``.
    """
    for name, arg in (("value", value), ("low", low), ("high", high)):
        if isinstance(arg, bool) or not isinstance(arg, (int, float)):
            raise TypeError(f"{name} must be an int or float")
    if low > high:
        raise ValueError("low must not be greater than high")
    return min(max(value, low), high)
