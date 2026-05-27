SCALES = ("celsius", "fahrenheit", "kelvin")


def convert(value: float, from_scale: str, to_scale: str) -> float:
    """Convert a temperature value between scales."""
    from_scale = from_scale.lower()
    to_scale = to_scale.lower()

    if from_scale not in SCALES or to_scale not in SCALES:
        raise ValueError(f"Scale must be one of {SCALES}")

    if from_scale == to_scale:
        return value

    # Convert to Celsius first
    if from_scale == "fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_scale == "kelvin":
        celsius = value - 273.15
    else:
        celsius = value

    # Convert from Celsius to target
    if to_scale == "fahrenheit":
        return celsius * 9 / 5 + 32
    elif to_scale == "kelvin":
        return celsius + 273.15
    else:
        return celsius
