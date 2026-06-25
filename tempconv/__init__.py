"""Convert temperatures between Celsius, Fahrenheit, Kelvin, Rankine, Réaumur and Newton."""

from .converter import SCALES, convert

__all__ = ["convert", "SCALES"]
