# tg-devices

**tg-devices** is a high-fidelity Python library designed to generate realistic, statistically plausible, and technically compatible device profiles for Telegram clients. It simulates hardware and software signatures across Windows, macOS, Linux, and Android.

## Project Overview

- **Core Goal**: Generate `DeviceProfile` objects that are believable and technically valid for Telegram's backend.
- **Key Technologies**: Python 3.14+, `uv` (package manager), `ruff` (linting/formatting), `mypy` (strict type checking), `pytest`.
- **Architecture**: Layered design using Protocol-based dependency injection.
    - `enums/`: Type-safe definitions for OS, hardware, and versions.
    - `weight/`: Management of probability distributions using the Largest Remainder Method.
    - `random/`: Abstraction for randomness (supports seeding).
    - `compatibility/`: Logic for version matching and pre-computed compatibility maps.
    - `generator/`: High-level API orchestrating all layers.

## Building and Running

This project uses `uv` for dependency management and `hatchling` as the build backend.

### Development Setup
```bash
uv sync
pre-commit install
```

### Running Tests
```bash
uv run pytest tests/ -v
# With coverage
uv run pytest tests/ --cov=tg_devices
```

### Quality Assurance
```bash
# Linting
uv run ruff check .
# Formatting
uv run ruff format .
# Type Checking
uv run mypy .
```

### Building the Package
```bash
uv build
```

## Development Conventions

### Code Style
- **Strict Typing**: The project uses `mypy --strict`. All function signatures must be fully typed.
- **Immutability**: Core data structures like `DeviceProfile` and `OSProfile` are frozen dataclasses.
- **Naming**: Follows standard Python (PEP 8) conventions. Enums use `SCREAMING_SNAKE_CASE` for members and `PascalCase` for the class.
- **Documentation**: Use Google-style docstrings for classes and methods.

### Testing Practices
- **Verifiability**: Every new feature or bug fix must be accompanied by tests in the `tests/` directory.
- **Compatibility**: Ensure that new app versions or system versions are added to the compatibility logic in `tg_devices/compatibility/inspection.py`.

### Contribution Guidelines
- Always run `pre-commit run --all-files` before pushing changes.
- Ensure 100% type safety and linting compliance.
- Update `tg_devices/__meta__.py` for version changes (handled via Hatch).

## Data Inventory
The library contains extensive data for:
- **Windows**: 150+ models, build versions up to 25H2.
- **macOS**: Apple Silicon and Intel models, versions up to 26.x.
- **Linux**: Kernel versions and distro-specific signatures.
- **Android**: 100+ models, versions up to Android 17.0.
- **Telegram**: App versions from 4.x to 12.x (including projections).
