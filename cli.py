"""Command-line interface for the temperature converter."""

import argparse

from converter import SCALES, convert


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="convert",
        description="Convert a temperature between Celsius, Fahrenheit and Kelvin.",
    )
    parser.add_argument("value", type=float, help="Temperature value to convert")
    parser.add_argument(
        "from_scale", help=f"Source scale, one of: {', '.join(SCALES)}"
    )
    parser.add_argument(
        "to_scale", help=f"Target scale, one of: {', '.join(SCALES)}"
    )
    args = parser.parse_args(argv)

    try:
        result = convert(args.value, args.from_scale, args.to_scale)
    except ValueError as exc:
        parser.error(str(exc))

    print(result)


if __name__ == "__main__":
    main()
