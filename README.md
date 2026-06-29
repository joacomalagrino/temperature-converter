# Temperature Converter

A simple utility to convert temperatures between Celsius, Fahrenheit, Kelvin, Rankine, Réaumur and Newton.

## Installation

```bash
pip install .
```

This installs the `tempconv` package and a `tempconv` command.

## Usage

```python
from tempconv import convert

convert(100, "celsius", "fahrenheit")  # 212.0
convert(0, "celsius", "kelvin")        # 273.15
```

## Command line

```bash
tempconv 100 celsius fahrenheit   # 212.0
tempconv 32 fahrenheit kelvin     # 273.15
```

Scale names are case-insensitive. Valid scales: `celsius`, `fahrenheit`, `kelvin`, `rankine`, `reaumur`, `newton`.

Use `tempconv --version` to print the installed version.

## Development

```bash
pip install -r requirements.txt   # test runner
pip install -e ".[dev]"
pytest
```

## License

[MIT](LICENSE)
