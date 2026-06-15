# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-15

### Added
- Réaumur and Newton scales (six supported scales in total).

## [0.1.0] - 2026-06-15

### Added
- `tempconv` command-line interface (installable via `pip install .`).
- Rankine scale.
- Packaging metadata (`pyproject.toml`) and MIT `LICENSE`.
- Test suite covering all conversions, round-trips, case-insensitivity and error cases.
- GitHub Actions CI across Python 3.11–3.13.

### Changed
- CLI output is rounded for display to avoid floating-point noise; the library keeps full precision.

### Fixed
- README typos.
- Added the `requirements.txt` referenced by the install instructions.

[0.2.0]: https://github.com/joacomalagrino/temperature-converter/releases/tag/v0.2.0
[0.1.0]: https://github.com/joacomalagrino/temperature-converter/releases/tag/v0.1.0
