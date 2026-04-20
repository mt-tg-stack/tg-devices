##########
tg-devices
##########

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT License

.. image:: https://img.shields.io/badge/python-3.14+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.14+

.. image:: https://img.shields.io/badge/mypy-strict-blue.svg
   :target: https://mypy-lang.org/
   :alt: Mypy Strict

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff
   :alt: Ruff

.. image:: https://img.shields.io/badge/tests-152%20passed-brightgreen.svg
   :target: https://github.com/mt-tg-stack/tg-devices/actions
   :alt: 152 Tests Passed

**tg-devices** is a high-fidelity Python library designed to generate realistic,
statistically plausible, and technically compatible device profiles for Telegram clients.

It simulates the hardware and software signatures of real-world Telegram users across
**Windows**, **macOS**, **Linux**, and **Android**, ensuring that generated combinations
of OS versions, app versions, and device models are both believable and technically valid.

.. contents:: Table of Contents
   :depth: 3
   :local:
   :backlinks: none

----

Key Capabilities
================

Realistic Statistical Simulation
---------------------------------

Uses weighted random generation based on real-world market share data. Distributions
for OSes, system versions, and app versions reflect actual global usage patterns.

Full Cross-Platform Support
----------------------------

Deep support for four major platforms with platform-specific signatures:

- **Windows**: Thousands of hardware IDs (Dell, HP, ASUS, etc.) and precise build numbers.
- **macOS**: Detailed Apple Silicon (M1–M4) and Intel hardware models.
- **Linux**: Kernel versions across major distros (Ubuntu, Arch, Fedora, Debian) and specific laptop models.
- **Android**: Comprehensive mobile device database including projected 2026 flagships.

Intelligent Compatibility Engine
----------------------------------

A sophisticated verification layer ensures that generated profiles are technically valid:

- Enforces minimum OS requirements for modern Telegram versions.
- Excludes legacy app versions from modern operating systems.
- Handles platform-specific architecture suffixes (``x64``, ``arm64``).

Future-Proof Hardware Database
--------------------------------

Includes data for current hardware and projections for **2025–2026**:

- Samsung Galaxy S26, Google Pixel 11, etc.
- Windows 11 25H2 and macOS Tahoe 26.x.

Enterprise-Grade Quality
-------------------------

- **Type Safety**: Built with strict static type checking (``mypy --strict``).
- **Immutability**: Uses frozen dataclasses to prevent runtime side effects.
- **Performance**: Pre-computed compatibility maps for O(1) runtime generation.

----

Installation
============

Requirements
------------

- **Python**: 3.14+ (Bleeding Edge)
- **Package Manager**: ``uv`` (recommended) or ``pip``

Standard Install
----------------

.. code-block:: bash

   # Using uv (recommended)
   uv add tg-devices

   # Using pip
   pip install tg-devices

Development Install
-------------------

.. code-block:: bash

   uv sync
   pre-commit install

----

Architecture & Design
======================

The library is designed using a clean, layered architecture with Protocol-based
dependency injection.

Layered Structure
-----------------

1. **Enums Layer** (``enums/``): Defines the "vocabulary" of the library. Every OS,
   hardware model, and version is a type-safe enum member.
2. **Weight Layer** (``weight/``): Manages probability distributions. Uses the
   **Largest Remainder Method (Hare-Niemeyer)** to ensure weights always sum to
   exactly 100% without rounding errors.
3. **Random Layer** (``random/``): Provides an abstraction for randomness, allowing
   for deterministic seeding or custom randomness sources.
4. **Compatibility Layer** (``compatibility/``): Contains the logic for version
   matching and the pre-computed compatibility maps.
5. **Generator Layer** (``generator/``): The high-level API that orchestrates the
   layers to produce a ``DeviceProfile``.

Core Protocols
--------------

The library relies on two primary protocols for extensibility:

- ``IRandomProvider``: Interface for selecting items from a population.
- ``IWeightProvider``: Interface for retrieving OS weights and compatibility data.

----

API Reference
=============

DeviceProfileGenerator
-----------------------

The main entry point for the library.

.. code-block:: python

   class DeviceProfileGenerator(IDeviceProfileGenerator):
       def __init__(
           self,
           random_provider: IRandomProvider | None = None,
           weight_provider: IWeightProvider | None = None,
           **weight_params: Unpack[WeightParams],
       ) -> None: ...

       def generate_device_profile(self, os: OS | None = None) -> DeviceProfile: ...

DeviceProfile
-------------

The immutable result of a generation.

.. code-block:: python

   @dataclass(frozen=True)
   class DeviceProfile:
       os: str             # "Windows", "macOS", "Linux", or "Android"
       app_version: str    # e.g., "6.0.2 x64"
       system_version: str # e.g., "10.0.22631"
       device_model: str   # e.g., "XPS 15 9530"

----

Usage Examples
==============

Basic Generation
----------------

.. code-block:: python

   from tg_devices import DeviceProfileGenerator

   generator = DeviceProfileGenerator()
   profile = generator.generate_device_profile()

   print(f"OS: {profile.os} | App: {profile.app_version}")

Custom OS Distribution
----------------------

Force specific OS probabilities. Missing keys are redistributed proportionally using LRM.

.. code-block:: python

   # 80% Android, remaining 20% distributed among others
   generator = DeviceProfileGenerator(android=80)

   # Force only desktop platforms
   generator = DeviceProfileGenerator(
       windows=40, macos=40, linux=20, android=0
   )

Seeded Reproducibility
----------------------

Generate identical profiles across different runs or machines.

.. code-block:: python

   from tg_devices.random.provider import StandardRandomProvider

   seed = 42
   gen = DeviceProfileGenerator(
       random_provider=StandardRandomProvider(seed=seed)
   )
   profile = gen.generate_device_profile()  # Always the same for seed 42

Manual Compatibility Check
--------------------------

Access the internal engine to verify your own version combinations.

.. code-block:: python

   from tg_devices import OS
   from tg_devices.compatibility.inspection import is_compatible

   # Returns False: Telegram 6.x requires Windows 7+
   is_compatible(OS.WINDOWS, "6.0", "6.0.0")

   # Returns True
   is_compatible(OS.WINDOWS, "10.0.19045", "6.0.0")

----

Data Inventory
==============

The library includes an extensive set of pre-defined data:

- **Windows**: 150+ hardware models (Dell, HP, ASUS, Lenovo, MSI, Gigabyte, Acer,
  Samsung, Surface), 15+ major build versions.
- **macOS**: 40+ hardware models (MacBook Pro/Air, Mac Mini, iMac, Mac Studio, Mac Pro),
  versions from 10.13 to 26.x.
- **Linux**: 50+ hardware models (ThinkPad, XPS, Framework, System76, Tuxedo),
  70+ kernel versions across 10+ distributions.
- **Android**: 100+ hardware models (Samsung, Google, Xiaomi, OnePlus, Nothing,
  Motorola, Sony), versions from Android 6.0 to 17.0.
- **Telegram Versions**: Comprehensive list of versions from 4.x to 12.x (including predictions).

----

Testing
=======

This project maintains a 100% success rate across 59+ comprehensive tests.

.. code-block:: bash

   # Run all tests
   uv run pytest tests/ -v

   # With coverage
   uv run pytest tests/ --cov=tg_devices

----

Development Standards
=====================

- **Linting/Formatting**: Handled by Ruff (``uv run ruff check .`` and ``uv run ruff format .``).
- **Type Checking**: Strict Mypy (``uv run mypy .``).
- **Pre-commit**: Hooks for all quality checks (``pre-commit run --all-files``).

----

License
=======

This project is licensed under the MIT License — see the `LICENSE <LICENSE>`_ file for details.

Authors
=======

- **GrehBan** — `maximfeedback19@gmail.com <mailto:maximfeedback19@gmail.com>`_

----

*Made with* ❤️ *by* `mt-tg-stack <https://github.com/mt-tg-stack>`_ *organization.*
