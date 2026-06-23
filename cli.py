"""Command-line interface for the temperature converter."""

import argparse

from converter import SCALES, convert


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="tempconv",
        description="Convert a temperature between any of the six supported scales.",
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

    # Round for display to avoid floating-point noise (e.g. 491.6699999996).
    # The library keeps full precision; only the printed value is tidied up.
    print(round(result, 6))


if __name__ == "__main__":
    main()
