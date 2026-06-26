"""Convert temperatures between Celsius, Fahrenheit, Kelvin, Rankine, Réaumur and Newton."""

from importlib.metadata import PackageNotFoundError, version

from .converter import SCALES, convert

try:
    __version__ = version("temperature-converter")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0+unknown"

__all__ = ["convert", "SCALES", "__version__"]
