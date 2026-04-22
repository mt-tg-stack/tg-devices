#########
Changelog
#########

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

0.1.5 - 2026-04-20
==================

This release introduces a **sophisticated weight precomputation engine** based on Gaussian distribution curves and significantly expands the test suite to ensure statistical accuracy and naming consistency.

Breaking Changes
----------------

- **Renamed internal weight constants**: Unified naming convention for all pre-computed OS weight data in ``tg_devices/weight/introspection/``.
  - Example: ``ANDROID_APPS`` -> ``ANDROID_APP_VERSIONS``, ``MAC_APPS_WEIGHTS`` -> ``MACOS_APP_WEIGHTS``, etc.
- **Dynamic Weight Precomputation**: Switched from hardcoded weight dictionaries to dynamic generation using Gaussian curves in the introspection layer.
- **Updated introspection exports**: Cleaned up ``tg_devices/weight/introspection/__init__.py`` to use grouped imports and explicit ``__all__``.

Added
-----

- **Gaussian Weight Engine**:
  - New module ``tg_devices.weight.introspection.weight_precomputation`` for generating statistically plausible version distributions.
  - Support for custom ``WeightCurveParams`` (peak ratio, sigma spread, max/min weights).
  - Specialized defaults for every supported platform (Windows, macOS, Linux, Android) for both apps and system versions.
- **Major Test Suite Expansion**:
  - Increased test count from 59 to **152 tests**.
  - New comprehensive tests for weight curves, peak positioning, and distribution boundaries.
  - Rigorous verification of version sorting and peer-group handling in weight calculation.

Changed
-------

- **Code Cleanup**: Removed redundant ``as`` aliases in internal re-exports.
- **Internal Consistency**: Standardized OS prefixes across all weight introspection files (e.g., always using ``LINUX_`` instead of ``LIN_``).
- **Documentation**: Updated README badges and testing sections to reflect the expanded coverage.

Fixed
-----

- **Weight Inconsistencies**: Resolved mixed naming styles and manual weight errors by switching to automated curve-based generation.
- **Distribution Shape**: Improved the realism of version distribution—users now statistically lag behind the latest releases in a way that matches real-world patterns.

Testing
~~~~~~~

.. code-block:: text

    ✅ 152 tests passed in 0.40 seconds

    Test Coverage Breakdown:
    - Weight Curve Logic: 25+ tests
    - OS-specific Distributions: 40+ tests
    - Version Compatibility: 50+ tests
    - Generator Integration: 20+ tests
    - Edge Cases & Protocols: 15+ tests

0.1.4 - 2026-04-17
==================

This release focuses on **refactoring and API clarification**, ensuring consistent naming across the library and better aligning terminology with the generated output.

Breaking Changes
----------------

- **Renamed OSProfile to DeviceProfile**: The dataclass representing the final generated profile was renamed for clarity.
- **Renamed generate_os_profile to generate_device_profile**: The main generation method in ``DeviceProfileGenerator`` was renamed to match the new profile class name.
- **Renamed StaticOSWeights to OSProfile**: The internal data bundle for each OS was renamed to ``OSProfile``.
- **Renamed Weights to VersionWeights**: The version-level weight container was renamed to ``VersionWeights``.

Added
-----

- **New Protocols**: Introduced ``IVersionWeight`` and ``IOSProfile`` to formalize internal data structures.
- **Type Aliases**: Added ``CompatibilityMap`` in ``tg_devices/compatibility/map.py`` for cleaner type signatures.

Changed
-------

- **API Consistency**: Updated ``IDeviceProfileGenerator`` and ``IWeightProvider`` protocols to use new naming conventions.
- **Documentation**: Updated all docstrings and examples to reflect the new API.
- **Type Hints**: Improved type hints throughout the ``generator`` and ``weight`` modules.

Fixed
-----

- **Docstring inaccuracies**: Corrected descriptions of return types in protocols and implementations.
- **Protocol alignment**: Ensured all providers strictly adhere to updated protocols.

Migration Guide from v0.1.3
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following changes are required to migrate code from v0.1.3 to v0.1.4:

**Updating imports:**

.. code-block:: python

    # v0.1.3
    from tg_devices import OSProfile

    # v0.1.4
    from tg_devices import DeviceProfile

**Updating method calls:**

.. code-block:: python

    # v0.1.3
    profile = generator.generate_os_profile()

    # v0.1.4
    profile = generator.generate_device_profile()

0.1.3 - 2026-04-16
==================

This release introduces a **comprehensive test suite**, **improved error handling**, and **bug fixes** to make the library production-ready.

Added
-----

- **Largest Remainder Method (LRM)**:
  - Implemented the Hare-Niemeyer algorithm for weight distribution.
  - Ensures weights always sum to exactly 100% without rounding errors.
  - Handles proportional redistribution for partial weight specifications.

- **Comprehensive Test Suite (59+ tests)**:

  - Basic functionality tests (profile generation, OS-specific generation)
  - Weight override tests (partial specification, complete specification)
  - Weight validation tests (exceeding 100, incomplete sum)
  - Seed consistency tests (reproducibility verification)
  - Linux compatibility tests (7 parameterized tests)
  - Windows compatibility tests (9 tests covering versions 6.0-11+)
  - macOS compatibility tests (8 tests covering versions 10.12-14+)
  - Android compatibility tests (13+ parameterized tests with comprehensive matrix)
  - Integration tests (generated profile compatibility verification)
  - Edge case tests (all OSes generation, immutability, zero weights)

- **Extended Documentation**:

  - Comprehensive docstrings for all modules and public APIs
  - Expanded README with version compatibility matrices
  - Architecture documentation explaining layer-based design
  - FAQ section addressing common use cases
  - Migration guide from v0.1.2

- **Improved Error Messages**:

  - Context-rich error messages with actual vs. expected values
  - Better validation error descriptions
  - Helpful suggestions in exception messages

- **Version Compatibility Documentation**:

  - Windows: detailed version requirements (Vista, 7, 10, 11)
  - macOS: version requirements from 10.12 to 14+
  - Android: version requirements from 5.0 to 15.0+
  - Linux: comprehensive compatibility matrix

Changed
-------

- **Weight Validation Logic Fix**:

  - Changed validation condition from ``if provided_sum >= 100`` to ``if provided_sum > 100``
  - Now correctly allows ``sum(weights) == 100`` with zero remainder
  - Fixes edge case where ``DeviceProfileGenerator(windows=10, android=90)`` incorrectly raised ValueError

- **Error Handling**:

  - Improved error context in weight distribution
  - Better messages for boundary condition violations
  - Clear indication of what went wrong and why

- **Documentation Structure**:

  - Reorganized README sections for better flow
  - Added badges for test coverage status
  - Improved code example formatting
  - Added version compatibility tables for visual reference

- **Test Organization**:

  - Organized tests into logical categories by functionality
  - Used ``pytest.mark.parametrize`` to eliminate test duplication
  - Comprehensive test docstrings explaining intent

Fixed
-----

- **Weight Validation Bug**:

  - Previously: ``DeviceProfileGenerator(windows=10, android=90)`` raised ValueError
  - Now: Correctly handles partial weights that sum to 100 with zero remainder
  - Properly distributes remaining weight (0) between unspecified OSes

- **Edge Case: Zero Weight**:

  - Now correctly excludes OS with weight=0 from generation
  - Verified through test: ``test_weight_zero_excludes_os``

- **Edge Case: All Weights Specified**:

  - Proper validation when all 4 OS weights are explicitly provided
  - Must sum to exactly 100 (no auto-distribution)

- **Integration Issues**:

  - All generated profiles now verified for version compatibility
  - No generation of impossible OS/version combinations

Testing
~~~~~~~

.. code-block:: text

    ✅ 59 tests passed in 0.37 seconds

    Test Coverage Breakdown:
    - Basic functionality: 3 tests
    - Weight distribution: 3 tests
    - Weight validation: 2 tests
    - Seed consistency: 2 tests
    - Linux compatibility: 7 tests
    - Windows compatibility: 9 tests
    - macOS compatibility: 8 tests
    - Android compatibility: 13 tests
    - Integration compatibility: 2 tests
    - Edge cases: 4 tests
    - Comprehensive Android matrix: 5 tests

Quality Metrics
~~~~~~~~~~~~~~~

- **Type Safety**: 100% mypy --strict compliance
- **Code Quality**: Ruff linting with zero violations
- **Test Coverage**: All public APIs covered with positive and negative tests
- **Documentation**: 100% of public APIs documented with comprehensive docstrings

Migration Guide from v0.1.2
~~~~~~~~~~~~~~~~~~~~~~~~~~~

✅ **No Breaking Changes** - All v0.1.2 code continues to work.

Previously Broken (v0.1.2):

.. code-block:: python

    # ❌ ValueError: Sum of provided weights (100) >= 100, but keys ['macos', 'linux'] are missing.
    gen = DeviceProfileGenerator(windows=10, android=90)

Now Works (v0.1.3):

.. code-block:: python

    # ✅ Works! macOS and Linux get weight=0
    gen = DeviceProfileGenerator(windows=10, android=90)

Backward Compatibility
~~~~~~~~~~~~~~~~~~~~~~

- ✅ All existing code from v0.1.2 works without modification
- ✅ All public APIs remain unchanged
- ✅ Default behavior unchanged (Windows 30%, macOS 15%, Linux 5%, Android 50%)
- ✅ Profile structure (OSProfile) unchanged
- ✅ Weight distribution algorithm unchanged (except bug fix)

Known Limitations
~~~~~~~~~~~~~~~~~

1. Limited device model coverage for older systems
   - Windows Vista/7 models are representative but not exhaustive
   - macOS 10.x models are representative but limited
   - Planned expansion in future releases

0.1.2 - 2026-02-25
==================

Added
-----

- **Public Re-exports**: ``DeviceProfileGenerator``, ``OS``, ``OSProfile`` are now importable directly from ``tg_devices`` package
- **Google-style Docstrings**: Comprehensive documentation across all modules, classes, and public functions
- **Module-level Docstrings**: Added to all ``__init__.py`` files for context and examples

Changed
-------

- **Compatibility Engine Overhaul**:

  - Replaced fragile positional index checks with semantic version parsing
  - Removed ``sys_idx`` and ``app_idx`` parameters
  - Now uses ``parse_version()`` for robust version comparison

- **Error Handling**:

  - ``get_compatibility_map()`` now raises ``ValueError`` instead of silently falling back to all apps

- **Code Quality**:

  - Removed ``# type: ignore`` comments from ``StaticWeightProvider.__init__``
  - Eliminated redundant ``cast`` calls
  - Simplified ``Unpack[TypedDict]`` kwargs handling

- **Generator API**:

  - ``DeviceProfileGenerator`` now forwards ``**weight_params: Unpack[WeightParams]`` to ``StaticWeightProvider``
  - Enables convenient API: ``DeviceProfileGenerator(windows=40, android=60)``

0.1.1 - 2026-02-25
==================

Added
-----

- **Weight Customization**:

  - New ``WeightParams`` ``TypedDict`` for type-safe weight configuration
  - ``StaticWeightProvider`` accepts ``**weight_params: Unpack[WeightParams]``
  - Proportional distribution of remaining budget for partial specifications
  - Example: ``StaticWeightProvider(windows=40, android=60)`` auto-distributes remaining 20%

- **Pre-computed Data**:

  - Pre-computed compatibility maps at module level:

    - ``WINDOWS_COMPATIBILITY_MAP``
    - ``MACOS_COMPATIBILITY_MAP``
    - ``LINUX_COMPATIBILITY_MAP``
    - ``ANDROID_COMPATIBILITY_MAP``

  - Pre-computed weight instances:

    - ``WINDOWS_WEIGHTS_DT``
    - ``MACOS_WEIGHTS_DT``
    - ``LINUX_WEIGHTS_DT``
    - ``ANDROID_WEIGHTS_DT``

  - Pre-computed device model tuples:

    - ``WINDOWS_DEVICE_MODEL``
    - ``MACOS_DEVICE_MODEL``
    - ``LINUX_DEVICE_MODEL``
    - ``ANDROID_DEVICE_MODEL``
    - ``OS_NAMES``

- **Type Safety**:

  - ``py.typed`` marker file for PEP 561 compliance
  - Package now advertises inline type information to consumers

Changed
-------

- **Provider Architecture**:

  - ``StaticWeightProvider.map`` and ``os_probabilities`` now instance attributes
  - Built inside ``__init__`` instead of class-level
  - Enables per-instance weight configuration

- **Type Annotations**:

  - All weight mapping constants annotated with ``Final``
  - Explicit ``tuple(dict.keys())`` / ``tuple(dict.values())`` instead of ``zip(*dict.items())``
  - Each tuple call annotated with ``Final``

- **Performance**:

  - Reduced computation time via pre-computed compatibility maps
  - Eliminated redundant version compatibility checks

Removed
-------

- ``uv.lock`` removed from version control (``uv sync`` manages lock file locally)

0.1.0 - 2026-02-24
==================

Initial Release
---------------

This is the first stable release of ``tg-devices``.

Added
-----

- **Core Generator**:

  - ``DeviceProfileGenerator`` class for creating realistic device profiles
  - Generates profiles combining OS, system version, app version, and device model

- **Operating System Support**:

  - Windows (6.0 - 11+)
  - macOS (10.12 - 14+)
  - Linux (5.4+)
  - Android (6.0 - 17.0, including projected 2026 devices)

- **Device Models**:

  - Comprehensive database of thousands of device models
  - Legacy hardware support (Windows Vista era devices)
  - Current generation devices
  - Projected 2026 flagships:

    - Samsung Galaxy S26, S26 Ultra
    - Google Pixel 11, 11 Pro
    - And many others

- **Android Version Coverage**:

  - Historical versions: Android 6.0 through 15.0
  - Future projections: Android 16.0, 17.0, 18.0, 19.0, 20.0

- **Telegram Application Versions**:

  - Desktop versions: 4.8.x through 6.5.x
  - Android versions: 9.x through 15.x
  - macOS/Windows/Linux versions with full history

- **Weighted Random Generation**:

  - Real-world market share data integration
  - Configurable per-OS weight distribution
  - Default weights: Windows 30%, macOS 15%, Linux 5%, Android 50%

- **Compatibility Engine**:

  - Intelligent version compatibility verification
  - Prevents impossible combinations (e.g., old apps on new OSs)
  - Real-world rules:

    - Telegram 6.x requires Windows 7+ or macOS 10.13+
    - Telegram 10.x requires Android 6.0+
    - Legacy apps excluded from modern systems

- **Type Safety**:

  - Complete type hints throughout codebase
  - Strict mypy configuration (``mypy --strict``)
  - Protocol-based dependency injection:

    - ``IRandomProvider`` for randomness sources
    - ``IWeightProvider`` for weight distributions
    - ``IDeviceProfileGenerator`` for generator interface

- **Enums for Type Safety**:

  - ``OS`` - Operating systems
  - ``DeviceModel`` - Hardware identifiers
  - ``SystemVersion`` - OS-specific versions
  - ``AppVersion`` - Telegram application versions
  - ``Weights`` - Probability distributions

- **Data Structures**:

  - ``OSProfile`` - Frozen dataclass for immutable profile output
  - ``WeightParams`` - TypedDict for weight configuration
  - ``StaticOSWeights`` - Bundle of OS-specific data

- **Development Tools**:

  - ``uv`` integration for modern Python package management
  - Strict mypy configuration for static type checking
  - Comprehensive ruff linting rules
  - Pre-commit hooks configuration

- **Documentation**:

  - Comprehensive README with examples
  - Module and function docstrings
  - Changelog tracking all changes
  - License and author information

- **Python Support**:

  - Python 3.14+ (Bleeding Edge)
  - Access to latest Python features

Fixed
-----

- **Directory Naming**:

  - Fixed typo: renamed ``tg_devices/copmatibility`` to ``tg_devices/compatibility``

- **Type Annotations**:

  - Resolved type annotation issues in ``tg_devices/weight/provider.py``
  - Satisfied strict mypy type checking requirements

- **Code Style**:

  - Corrected line length violations in introspection data files
  - Adheres to PEP 8 standards

Version Compatibility
~~~~~~~~~~~~~~~~~~~~~

This release establishes the version compatibility rules that are maintained in future releases:

**Windows Requirements:**

- Telegram 6.x requires Windows 7+ (version 6.1)
- Telegram 8.x+ require Windows 10 build 2004+

**macOS Requirements:**

- Telegram 6.x+ require macOS 10.13 (High Sierra)+

**Android Requirements:**

- Telegram 10.x requires Android 6.0+
- Telegram 11.x requires Android 7.0+
- Telegram 12.x+ require Android 8.0+

**Linux:**

- No specific version requirements
- All Telegram versions compatible with Linux 5.4+

Feature Comparison vs. Similar Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Feature | tg-devices | Faker | Mimesis |
|---------|:----------:|:-----:|:-------:|
| **Telegram profiles** | ✅ | ❌ | ❌ |
| **Version compatibility** | ✅ | ❌ | ❌ |
| **Cross-platform** | ✅ | ✅ | ✅ |
| **Type safety** | ✅ Strict | ⚠️ Partial | ⚠️ Partial |
| **Reproducible** | ✅ | ✅ | ✅ |
| **Extensible** | ✅ Protocols | ⚠️ Limited | ⚠️ Limited |

---

Versioning Strategy
===================

This project follows `Semantic Versioning <https://semver.org/>`_:

- **MAJOR**: Incompatible API changes
- **MINOR**: New backwards-compatible features
- **PATCH**: Bug fixes and improvements

Current Status: **v0.1.x** (Pre-v1.0, active development)

- API may change between minor versions
- Deprecation warnings provided when possible
- v1.0.0 will indicate API stability

---

Contributing
============

When reporting issues or suggesting features, please consider the version impact:

- **Bug fixes**: Patch version (v0.1.x → v0.1.(x+1))
- **New features**: Minor version (v0.1.x → v0.(1+1).0)
- **Breaking changes**: Major version (v0.x.x → v1.0.0)

---

Additional Resources
====================

- `GitHub Repository <https://github.com/mt-tg-stack/tg-devices>`_
- `PyPI Package <https://pypi.org/project/tg-devices/>`_
- `Keep a Changelog <https://keepachangelog.com/>`_
- `Semantic Versioning <https://semver.org/>`_
