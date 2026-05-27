from converter import convert


def test_celsius_to_fahrenheit():
    assert convert(100, "celsius", "fahrenheit") == 212.0


def test_fahrenheit_to_celsius():
    assert convert(32, "fahrenheit", "celsius") == 0.0


def test_celsius_to_kelvin():
    assert convert(0, "celsius", "kelvin") == 273.15


def test_same_scale_returns_value():
    assert convert(42, "celsius", "celsius") == 42
