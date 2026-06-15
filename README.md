# Temperature Converter

A simple utility to convert temperatures between Celsius, Fahrenheit, Kelvin and Rankine.

## Usage

```python
from converter import convert

convert(100, "celsius", "fahrenheit")  # 212.0
convert(0, "celsius", "kelvin")        # 273.15
```

## Command line

```bash
python cli.py 100 celsius fahrenheit   # 212.0
python cli.py 32 fahrenheit kelvin     # 273.15
```

Scale names are case-insensitive. Valid scales: `celsius`, `fahrenheit`, `kelvin`, `rankine`.

## Installation

```bash
pip install -r requirements.txt
```

### Install as a command

Installing the package adds a `tempconv` command:

```bash
pip install .
tempconv 100 celsius fahrenheit   # 212.0
```

## Running tests

```bash
pip install -e ".[dev]"
pytest
```

## License

[MIT](LICENSE)
