##########
tg-devices
##########

|License| |Python| |Mypy| |Ruff| |Tests|

**tg-devices** is a robust Python library designed to generate realistic, statistically plausible, and technically compatible device profiles for Telegram clients.

It simulates various operating systems (Windows, macOS, Linux, Android), system versions, app versions, and device models, ensuring that the generated combinations mirror real-world usage distributions and compatibility requirements.

.. contents:: Table of Contents
   :depth: 3
   :local:

✨ Features
===========

🎲 **Realistic Simulation**
  Uses weighted random generation based on real-world market share data to create believable device profiles.

🖥️ **Cross-Platform Support**
  Full support for **Windows**, **macOS**, **Linux**, and **Android** environments with hundreds of device models.

🔗 **Compatibility Engine**
  Intelligent verification logic ensures that generated App versions are strictly compatible with the selected System version:

  - Prevents legacy apps on new OSs
  - Enforces minimum version requirements
  - Handles real-world compatibility rules

💾 **Extensive Device Database**
  Includes thousands of device models:

  - Legacy hardware (Windows Vista, macOS 10.x)
  - Current generation devices
  - Projected 2026 flagships (Samsung Galaxy S26, Pixel 11, etc.)

🔒 **Type Safety**
  Built with strict static type checking (``mypy --strict``) for maximum reliability.

🏗️ **Modern Architecture**
  Protocol-based dependency injection for Randomness and Weight providers with specific Enums for every component.

🧪 **Production Ready**
  59+ comprehensive tests covering all functionality and edge cases.

What's New in v0.1.3
====================

Added
-----

- ✅ **Comprehensive Test Suite**: 59+ tests covering all functionality (basic, weight distribution, version compatibility, edge cases)
- ✅ **Extended Documentation**: Docstrings for all modules, classes, and public functions
- ✅ **Improved Error Handling**: Better error messages with context

Fixed
-----

- ✅ **Weight Validation**: Fixed condition to allow ``sum(weights) == 100`` with zero remainder
- ✅ **Edge Cases**: Proper handling of zero weights and boundary conditions
- ✅ **Reproducibility**: Guaranteed consistent results with seed values

Migration from v0.1.2
~~~~~~~~~~~~~~~~~~~~~

✅ **No Breaking Changes!** - Safe to upgrade.

**Previously broken (v0.1.2):**

.. code-block:: python

    # ❌ ValueError: "Sum of provided weights (100) >= 100"
    gen = DeviceProfileGenerator(windows=10, android=90)

**Now works in v0.1.3:**

.. code-block:: python

    # ✅ Works! Remainder distributes to macOS and Linux
    gen = DeviceProfileGenerator(windows=10, android=90)

Requirements
============

- **Python**: 3.14+ (Bleeding Edge)
- **Package Manager**: ``uv`` (recommended) or ``pip``

Installation
============

PyPI (Recommended)
------------------

.. code-block:: bash

    # Using uv (Recommended)
    uv add tg-devices

    # Using pip
    pip install tg-devices

From Source
-----------

For development or latest features:

.. code-block:: bash

    # Using uv
    uv add git+https://github.com/mt-tg-stack/tg-devices.git

    # Using pip
    pip install git+https://github.com/mt-tg-stack/tg-devices.git

Quick Start
===========

Basic Generation
----------------

The simplest way to use ``tg-devices`` is to instantiate the generator and call ``generate_os_profile``.

.. code-block:: python

    from tg_devices import DeviceProfileGenerator

    # Initialize the generator
    generator = DeviceProfileGenerator()

    # Generate a random profile
    profile = generator.generate_os_profile()

    print(f"OS: {profile.os}")                 # e.g., "Windows"
    print(f"System: {profile.system_version}") # e.g., "Windows 10 22H2"
    print(f"App: {profile.app_version}")       # e.g., "6.0.2 x64"
    print(f"Device: {profile.device_model}")   # e.g., "Desktop"

Generate Profile for Specific OS
---------------------------------

Force the generator to produce a profile for a specific Operating System:

.. code-block:: python

    from tg_devices import DeviceProfileGenerator, OS

    generator = DeviceProfileGenerator()

    # Generate a macOS specific profile
    mac_profile = generator.generate_os_profile(os=OS.MACOS)
    print(f"Generated {mac_profile.os} running on {mac_profile.system_version}")

    # Generate an Android profile (includes projected 2026 devices)
    android_profile = generator.generate_os_profile(os=OS.ANDROID)
    print(f"Device: {android_profile.device_model}")  # e.g., "Samsung Galaxy S26 Ultra"

Custom OS Weight Distribution
------------------------------

By default, OS weights are:

- Windows: 30%
- macOS: 15%
- Linux: 5%
- Android: 50%

You can override them in three ways:

**Complete Specification (all OSes):**

.. code-block:: python

    from tg_devices import DeviceProfileGenerator

    # Fully custom weights (must sum to 100)
    generator = DeviceProfileGenerator(
        windows=50, macos=10, linux=5, android=35,
    )

**Partial Specification (auto-distributed):**

.. code-block:: python

    # Partial weights — the rest is distributed proportionally
    generator = DeviceProfileGenerator(android=80)
    # Windows, macOS, Linux get: 6, 3, 1 (proportional to defaults)

**Exclude an OS:**

.. code-block:: python

    # Force only Android
    generator = DeviceProfileGenerator(
        windows=0, macos=0, linux=0, android=100
    )

Reproducible Generation
-----------------------

Use seeds for deterministic, reproducible results:

.. code-block:: python

    from tg_devices import DeviceProfileGenerator
    from tg_devices.random.provider import StandardRandomProvider

    # Same seed → identical results
    gen1 = DeviceProfileGenerator(
        random_provider=StandardRandomProvider(seed=42)
    )
    profile1 = gen1.generate_os_profile()

    gen2 = DeviceProfileGenerator(
        random_provider=StandardRandomProvider(seed=42)
    )
    profile2 = gen2.generate_os_profile()

    assert profile1 == profile2  # ✅ True

Version Compatibility
---------------------

Check if a version combination is compatible:

.. code-block:: python

    from tg_devices import OS
    from tg_devices.compatibility.inspection import is_compatible

    # Telegram 6.x requires Windows 7+ (6.1)
    assert not is_compatible(OS.WINDOWS, "6.0", "6.0.0")      # ❌ Vista
    assert is_compatible(OS.WINDOWS, "6.1", "6.0.0")          # ✅ Windows 7

    # Telegram 10.x requires Android 6.0+
    assert not is_compatible(OS.ANDROID, "5.0", "10.0.0")     # ❌ Android 5.0
    assert is_compatible(OS.ANDROID, "6.0", "10.0.0")         # ✅ Android 6.0

    # Old apps don't appear on new systems
    assert not is_compatible(OS.WINDOWS, "10.0.22000", "4.8.0")  # ❌ Windows 11 + old app
    assert is_compatible(OS.WINDOWS, "10.0.22000", "6.0.0")      # ✅ Windows 11 + new app

Output Data Structure
---------------------

The generator returns an ``OSProfile`` dataclass (frozen and immutable):

.. code-block:: python

    from dataclasses import dataclass

    @dataclass(frozen=True)
    class OSProfile:
        os: str             # The Operating System name
        app_version: str    # The Telegram App version
        system_version: str # The specific OS version
        device_model: str   # The hardware model identifier

Version Compatibility Matrix
=============================

Windows Compatibility
---------------------

| Telegram | Windows Vista | Windows 7+ | Windows 10 2004+ | Windows 11 |
|----------|:-------------:|:----------:|:----------------:|:----------:|
| 4.x      | ❌            | ✅         | ✅               | ❌         |
| 5.x      | ❌            | ✅         | ✅               | ✅         |
| 6.x+     | ❌            | ✅         | ✅               | ✅         |

macOS Compatibility
-------------------

| Telegram | macOS 10.12 | macOS 10.13+ | macOS 11+ | macOS 14+ |
|----------|:-----------:|:------------:|:---------:|:---------:|
| 6.x      | ❌          | ✅           | ✅        | ✅        |
| 7.x+     | ❌          | ✅           | ✅        | ✅        |

Android Compatibility
---------------------

| Telegram | Android 5.x | Android 6.x | Android 7.x | Android 8.x+ |
|----------|:-----------:|:----------:|:----------:|:------------:|
| 9.x      | ✅          | ✅         | ✅        | ✅           |
| 10.x     | ❌          | ✅         | ✅        | ✅           |
| 11.x     | ❌          | ❌         | ✅        | ✅           |
| 12.x     | ❌          | ❌         | ❌        | ✅           |
| 13.x+    | ❌          | ❌         | ❌        | ✅           |

Linux Compatibility
-------------------

Linux has no specific version requirements. All Telegram versions are compatible with all tested Linux versions (5.4+).

Testing
=======

This project includes 59+ comprehensive tests covering:

- ✅ Basic functionality
- ✅ Weight distribution
- ✅ Version compatibility (all OSes)
- ✅ Reproducibility with seeds
- ✅ Edge cases and boundary conditions
- ✅ Integration scenarios

Running Tests
-------------

.. code-block:: bash

    # Run all tests
    uv run pytest tests/ -v

    # Run specific category
    uv run pytest tests/ -k "Android" -v

    # With coverage report
    uv run pytest tests/ --cov=tg_devices --cov-report=html

Test Results
~~~~~~~~~~~~

.. code-block:: text

    ===== 59 passed in 0.37s =====

    ✅ Basic functionality (3 tests)
    ✅ Weight overrides (3 tests)
    ✅ Weight validation (2 tests)
    ✅ Seed consistency (2 tests)
    ✅ Linux compatibility (7 tests)
    ✅ Windows compatibility (9 tests)
    ✅ macOS compatibility (8 tests)
    ✅ Android compatibility (13 tests)
    ✅ Integration tests (2 tests)
    ✅ Edge cases (4 tests)

Development
===========

This project uses `uv <https://github.com/astral-sh/uv>`_ for dependency management and workflow automation.

Setup
-----

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/mt-tg-stack/tg-devices.git
       cd tg-devices

2. Sync dependencies:

   .. code-block:: bash

       uv sync

3. Install pre-commit hooks:

   .. code-block:: bash

       pre-commit install

Code Quality
------------

We enforce strict code quality standards. Ensure all checks pass before committing.

**Linting & Formatting (Ruff):**

.. code-block:: bash

    uv run ruff check .
    uv run ruff format .

**Type Checking (Mypy):**

.. code-block:: bash

    uv run mypy .

**Pre-commit Hooks:**

.. code-block:: bash

    pre-commit run --all-files

Project Structure
-----------------

.. code-block:: text

    tg-devices/
    ├── tg_devices/
    │   ├── __init__.py                 # Public API
    │   ├── __meta__.py                 # Version info
    │   ├── py.typed                    # PEP 561 marker
    │   ├── enums/                      # Device enums
    │   │   ├── os.py
    │   │   ├── windows.py
    │   │   ├── macos.py
    │   │   ├── linux.py
    │   │   └── android.py
    │   ├── generator/                  # Generation logic
    │   │   ├── generator.py
    │   │   ├── profile.py
    │   │   └── protocols.py
    │   ├── weight/                     # Weight distribution
    │   │   ├── provider.py
    │   │   ├── protocols.py
    │   │   └── weights.py
    │   ├── random/                     # Randomness provider
    │   │   ├── provider.py
    │   │   └── protocols.py
    │   └── compatibility/              # Version compatibility
    │       ├── inspection.py
    │       └── map.py
    ├── tests/                          # Test suite (59+ tests)
    │   └── test_generator.py
    ├── pyproject.toml                  # Project configuration
    ├── README.rst                      # This file
    └── CHANGELOG.rst                   # Version history

Configuration Details
---------------------

**Python Version:**

The project targets Python 3.14+ (Bleeding Edge). This ensures access to latest Python features and security updates.

**Type Checking:**

All code is validated with ``mypy --strict``, including:

- Disallow any generics without parameters
- Disallow untyped function definitions
- Disallow incomplete type definitions
- Namespace packages enabled
- Return types checked

**Linting:**

Ruff configuration enforces:

- PEP 8 style (E, W)
- Pyflakes checks (F)
- Import sorting (I)
- Return value checks (RET)
- Quote consistency (Q)
- Comprehension optimization (C4)
- Python version upgrades (UP)

Architecture
============

The library is organized into distinct layers:

**Enums Layer** (``enums/``)
  Provides type-safe enumerations for:

  - Operating Systems (``OS``)
  - Device Models (``DeviceModel``)
  - System Versions (``SystemVersion``)
  - Application Versions (``AppVersion``)

**Weight Layer** (``weight/``)
  Manages probability distributions:

  - ``StaticWeightProvider``: Pre-computed weight distributions
  - ``WeightParams``: Type-safe weight configuration
  - Proportional weight distribution algorithm

**Random Layer** (``random/``)
  Protocol-based randomness injection:

  - ``IRandomProvider``: Interface for randomness sources
  - ``StandardRandomProvider``: Default implementation using ``random.Random``
  - Supports custom implementations for testing

**Generator Layer** (``generator/``)
  Core profile generation logic:

  - ``DeviceProfileGenerator``: Main API
  - ``OSProfile``: Output dataclass
  - ``IDeviceProfileGenerator``: Protocol for generator interface

**Compatibility Layer** (``compatibility/``)
  Version compatibility verification:

  - ``is_compatible()``: Checks OS/App version compatibility
  - Real-world rules and projections

FAQ
===

**Q: Why does generated profile OS not match OS percentage?**

A: With limited samples, statistical variance is expected. The percentages are probabilities, not guarantees. With 1000+ profiles, distributions match weights closely.

**Q: Can I use custom randomness source?**

A: Yes! Implement ``IRandomProvider`` and pass to ``DeviceProfileGenerator``:

   .. code-block:: python

       from tg_devices import DeviceProfileGenerator

       class MyRandomProvider(IRandomProvider):
           def choice(self, population, weights=None):
               # Your implementation
               pass

       gen = DeviceProfileGenerator(random_provider=MyRandomProvider())

**Q: Are generated profiles truly realistic?**

A: The library uses real-world market share data and official Telegram compatibility rules. However, it's a statistical simulation—edge cases may not be represented.

**Q: Is this safe for production?**

A: Yes! The library has:

- Strict type checking (mypy --strict)
- 59+ comprehensive tests
- Frozen dataclasses preventing mutations
- Protocol-based design allowing easy testing

**Q: How do I contribute?**

A: See our Contributing Guide (coming soon). For now:

   1. Fork the repository
   2. Create a feature branch
   3. Ensure all checks pass (ruff, mypy, pytest)
   4. Submit a pull request

Resources
=========

- `GitHub Repository <https://github.com/mt-tg-stack/tg-devices>`_
- `PyPI Package <https://pypi.org/project/tg-devices/>`_
- `Changelog <CHANGELOG.rst>`_
- `Telegram Bot API <https://core.telegram.org/bots/api>`_

License
=======

This project is licensed under the MIT License - see the `LICENSE <LICENSE>`_ file for details.

Authors
=======

- **GrehBan** - `maximfeedback19@gmail.com <mailto:maximfeedback19@gmail.com>`_

Contributing
============

Contributions are welcome! Please ensure:

1. All tests pass: ``uv run pytest tests/``
2. Type checking passes: ``uv run mypy .``
3. Code is formatted: ``uv run ruff format .``
4. Linting passes: ``uv run ruff check .``

Acknowledgments
===============

- `astral-sh/uv <https://github.com/astral-sh/uv>`_ - Package manager and task runner
- `astral-sh/ruff <https://github.com/astral-sh/ruff>`_ - Linter and formatter
- `python/mypy <https://github.com/python/mypy>`_ - Static type checker
- `python/pytest <https://github.com/pytest-dev/pytest>`_ - Testing framework

Support
=======

For issues, questions, or suggestions:

1. Check `Existing Issues <https://github.com/mt-tg-stack/tg-devices/issues>`_
2. Search `Discussions <https://github.com/mt-tg-stack/tg-devices/discussions>`_
3. Create a `New Issue <https://github.com/mt-tg-stack/tg-devices/issues/new>`_

---

|

**Made with ❤️ by `mt-tg-stack <https://github.com/mt-tg-stack>`_ organization**

.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT License

.. |Python| image:: https://img.shields.io/badge/python-3.14+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.14+

.. |Mypy| image:: https://img.shields.io/badge/mypy-strict-blue.svg
   :target: https://mypy-lang.org/
   :alt: Mypy Strict

.. |Ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff
   :alt: Ruff

.. |Tests| image:: https://img.shields.io/badge/tests-59%20passed-brightgreen.svg
   :target: https://github.com/mt-tg-stack/tg-devices/actions
   :alt: 59 Tests Passed
