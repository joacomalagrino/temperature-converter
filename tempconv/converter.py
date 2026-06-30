import math

SCALES = ("celsius", "fahrenheit", "kelvin", "rankine", "reaumur", "newton")


def _to_celsius(value: float, scale: str) -> float:
    """Convert *value* from *scale* to Celsius. *scale* must already be lowercase."""
    if scale == "fahrenheit":
        return (value - 32) * 5 / 9
    if scale == "kelvin":
        return value - 273.15
    if scale == "rankine":
        return value * 5 / 9 - 273.15
    if scale == "reaumur":
        return value * 5 / 4
    if scale == "newton":
        return value * 100 / 33
    return value  # celsius


def convert(value: float, from_scale: str, to_scale: str) -> float:
    """Convert a temperature value between scales."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(
            f"value must be a numeric type (int or float), got {type(value).__name__!r}"
        )
    if not math.isfinite(value):
        raise ValueError(f"value must be a finite number, got {value!r}")

    if not isinstance(from_scale, str) or not isinstance(to_scale, str):
        raise ValueError(
            "from_scale and to_scale must be strings, got "
            f"{type(from_scale).__name__!r} and {type(to_scale).__name__!r}"
        )

    from_scale = from_scale.lower()
    to_scale = to_scale.lower()

    if from_scale not in SCALES or to_scale not in SCALES:
        raise ValueError(f"Scale must be one of {SCALES}")

    if from_scale == to_scale:
        # Still validate absolute zero even on identity conversion.
        celsius_check = _to_celsius(value, from_scale)
        if celsius_check < -273.15 - 1e-9:
            raise ValueError(
                f"{value} {from_scale} is below absolute zero (-273.15 °C)"
            )
        return value

    # Convert to Celsius first
    celsius = _to_celsius(value, from_scale)

    if celsius < -273.15 - 1e-9:
        raise ValueError(
            f"{value} {from_scale} is below absolute zero (-273.15 °C)"
        )

    # Convert from Celsius to target
    if to_scale == "fahrenheit":
        result = celsius * 9 / 5 + 32
    elif to_scale == "kelvin":
        result = celsius + 273.15
    elif to_scale == "rankine":
        result = (celsius + 273.15) * 9 / 5
    elif to_scale == "reaumur":
        result = celsius * 4 / 5
    elif to_scale == "newton":
        result = celsius * 33 / 100
    else:
        result = celsius

    if not math.isfinite(result):
        raise ValueError(
            f"conversion of {value} {from_scale} to {to_scale} overflowed "
            "to a non-finite number"
        )
    return result
