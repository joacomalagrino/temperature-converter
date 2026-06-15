import pytest

import cli
from converter import SCALES, convert


# Known reference points: water freezing and boiling at 1 atm.
@pytest.mark.parametrize(
    "value, from_scale, to_scale, expected",
    [
        # Celsius -> Fahrenheit
        (0, "celsius", "fahrenheit", 32.0),
        (100, "celsius", "fahrenheit", 212.0),
        (-40, "celsius", "fahrenheit", -40.0),  # the scales cross here
        # Fahrenheit -> Celsius
        (32, "fahrenheit", "celsius", 0.0),
        (212, "fahrenheit", "celsius", 100.0),
        # Celsius <-> Kelvin
        (0, "celsius", "kelvin", 273.15),
        (273.15, "kelvin", "celsius", 0.0),
        (-273.15, "celsius", "kelvin", 0.0),  # absolute zero
        # Fahrenheit <-> Kelvin
        (32, "fahrenheit", "kelvin", 273.15),
        (273.15, "kelvin", "fahrenheit", 32.0),
        # Rankine (Fahrenheit-based absolute scale)
        (0, "celsius", "rankine", 491.67),
        (100, "celsius", "rankine", 671.67),
        (0, "rankine", "kelvin", 0.0),  # absolute zero
        (491.67, "rankine", "fahrenheit", 32.0),
        (671.67, "rankine", "celsius", 100.0),
    ],
)
def test_known_conversions(value, from_scale, to_scale, expected):
    assert convert(value, from_scale, to_scale) == pytest.approx(expected)


@pytest.mark.parametrize("scale", SCALES)
def test_same_scale_returns_value_unchanged(scale):
    assert convert(42, scale, scale) == 42


@pytest.mark.parametrize(
    "value, from_scale, to_scale",
    [
        (123.45, "celsius", "fahrenheit"),
        (-17.8, "fahrenheit", "kelvin"),
        (300, "kelvin", "celsius"),
    ],
)
def test_round_trip_is_lossless(value, from_scale, to_scale):
    """Converting there and back returns the original value."""
    there = convert(value, from_scale, to_scale)
    back = convert(there, to_scale, from_scale)
    assert back == pytest.approx(value)


def test_scale_names_are_case_insensitive():
    assert convert(100, "CELSIUS", "Fahrenheit") == pytest.approx(212.0)


@pytest.mark.parametrize(
    "from_scale, to_scale",
    [
        ("newton", "celsius"),
        ("celsius", "newton"),
        ("", "kelvin"),
    ],
)
def test_unknown_scale_raises_value_error(from_scale, to_scale):
    with pytest.raises(ValueError):
        convert(0, from_scale, to_scale)


def test_cli_prints_result(capsys):
    cli.main(["100", "celsius", "fahrenheit"])
    assert capsys.readouterr().out.strip() == "212.0"


def test_cli_tidies_floating_point_noise(capsys):
    cli.main(["0", "celsius", "rankine"])
    assert capsys.readouterr().out.strip() == "491.67"


def test_cli_unknown_scale_exits_with_code_2():
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["0", "newton", "celsius"])
    assert exc_info.value.code == 2
