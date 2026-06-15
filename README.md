# Temperature Converter

A simple utility to convert temperatures between Celsius, Fahrenheit and Kelvin.

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

Scale names are case-insensitive. Valid scales: `celsius`, `fahrenheit`, `kelvin`.

## Installation

```bash
pip install -r requirements.txt
```

## Running tests

```bash
pytest
```
