from importlib.metadata import version

import pytest

import tempconv
from tempconv import SCALES, convert
from tempconv import cli


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
        # Réaumur (water boils at 80 degrees)
        (100, "celsius", "reaumur", 80.0),
        (80, "reaumur", "celsius", 100.0),
        (0, "reaumur", "fahrenheit", 32.0),
        # Newton (water boils at 33 degrees)
        (100, "celsius", "newton", 33.0),
        (33, "newton", "celsius", 100.0),
        (0, "newton", "kelvin", 273.15),
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
        (50, "reaumur", "newton"),
        (20, "newton", "rankine"),
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
        ("bogus", "celsius"),
        ("celsius", "bogus"),
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
        cli.main(["0", "bogus", "celsius"])
    assert exc_info.value.code == 2


# --- Input validation tests ---


@pytest.mark.parametrize("bad_value", ["25", None, [], True, False])
def test_non_numeric_input_raises_value_error(bad_value):
    """Non-numeric inputs (including bool) must raise ValueError, not TypeError."""
    with pytest.raises(ValueError):
        convert(bad_value, "celsius", "fahrenheit")


@pytest.mark.parametrize("bad_value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_input_raises_value_error(bad_value):
    """NaN and Inf must raise ValueError."""
    with pytest.raises(ValueError):
        convert(bad_value, "celsius", "fahrenheit")


@pytest.mark.parametrize(
    "value, from_scale",
    [
        (-274, "celsius"),
        (-274.0, "celsius"),
        (-1000, "celsius"),
        (-459.68, "fahrenheit"),   # ≈ -273.16 °C, just below absolute zero
        (-1, "kelvin"),
        (-1, "rankine"),
        (-274, "reaumur"),
        (-91, "newton"),
    ],
)
def test_below_absolute_zero_raises_value_error(value, from_scale):
    """Temperatures below absolute zero must raise ValueError."""
    with pytest.raises(ValueError):
        convert(value, from_scale, "kelvin")


def test_absolute_zero_celsius_is_valid():
    """-273.15 °C is exactly absolute zero and must NOT raise."""
    result = convert(-273.15, "celsius", "kelvin")
    assert result == pytest.approx(0.0)


def test_absolute_zero_kelvin_is_valid():
    """0 K is exactly absolute zero and must NOT raise."""
    result = convert(0, "kelvin", "celsius")
    assert result == pytest.approx(-273.15)


@pytest.mark.parametrize("scale", SCALES)
def test_same_scale_below_absolute_zero_raises(scale):
    """Identity conversions must still reject values below absolute zero.

    Covers the early-return branch in ``convert`` where ``from == to``; a
    physically impossible temperature must raise even when no real conversion
    happens.
    """
    with pytest.raises(ValueError):
        convert(-1000, scale, scale)


@pytest.mark.parametrize(
    "scale, abs_zero",
    [
        ("celsius", -273.15),
        ("kelvin", 0.0),
        ("fahrenheit", -459.67),
        ("rankine", 0.0),
        ("reaumur", -218.52),
        ("newton", -90.1395),
    ],
)
def test_absolute_zero_per_scale_is_valid(scale, abs_zero):
    """Each scale's exact absolute-zero point converts to 0 K without raising."""
    assert convert(abs_zero, scale, "kelvin") == pytest.approx(0.0, abs=1e-9)


# --- Overflow regression test ---


@pytest.mark.parametrize(
    "value, from_scale, to_scale",
    [
        (1e308, "celsius", "rankine"),       # (c + 273.15) * 9/5 overflows
        (1.5e308, "celsius", "fahrenheit"),  # c * 9/5 + 32 overflows
        (1e308, "kelvin", "rankine"),        # overflows via the rankine factor
    ],
)
def test_finite_input_overflowing_to_inf_raises_value_error(value, from_scale, to_scale):
    """A finite input that overflows to inf must raise, not return inf silently."""
    with pytest.raises(ValueError):
        convert(value, from_scale, to_scale)


# --- Non-string scale regression test ---


@pytest.mark.parametrize("bad_scale", [123, None, 1.0, ["celsius"], object()])
def test_non_string_scale_raises_value_error(bad_scale):
    """A non-string scale must raise ValueError, not AttributeError."""
    with pytest.raises(ValueError):
        convert(0, bad_scale, "celsius")
    with pytest.raises(ValueError):
        convert(0, "celsius", bad_scale)


# --- Version exposure tests ---


def test_package_exposes_version():
    """tempconv.__version__ matches the installed package metadata."""
    assert tempconv.__version__ == version("temperature-converter")


def test_cli_version_flag(capsys):
    """`tempconv --version` prints the version and exits with code 0."""
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--version"])
    assert exc_info.value.code == 0
    assert capsys.readouterr().out.strip() == f"tempconv {tempconv.__version__}"
