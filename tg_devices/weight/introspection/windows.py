"""Pre-computed static weight data for Windows.

All constants in this module are computed **once at import time** and cached
as ``Final``. This is intentional:

- ``compute_weights`` runs a Gaussian curve over sorted enum members —
  O(n log n) due to sorting, but n is small (≤ 150 members per enum).
- ``get_compatibility_map`` iterates all (sys_ver × app_ver) pairs —
  O(n²) in enum sizes, again small and bounded.
- Total wall time across all four platforms is < 5 ms on modern hardware.

**Do not switch to lazy initialisation.** Deferring computation to first
access would cache results against the enum state at that moment. Any enum
member added after import but before first access would be silently excluded
from weight maps and compatibility checks — a data-consistency bug that is
hard to detect and reproduce.

If import-time cost becomes measurable (e.g. serverless cold starts), the
correct fix is to pre-build the data as a static artefact (JSON / pickle)
at package build time, not to defer computation to runtime.
"""

from collections.abc import Mapping
from typing import Final

from tg_devices.compatibility.map import get_compatibility_map
from tg_devices.enums.app_version import AppVersion
from tg_devices.enums.os import OS
from tg_devices.enums.system_version import SystemVersion
from tg_devices.enums.windows import (
    WindowsAppVersion,
    WindowsDesktopModel,
    WindowsSystemVersion,
)
from tg_devices.weight.introspection.weight_precomputation import (
    PLATFORM_DEFAULTS,
    WeightCurveParams,
    compute_weights,
)
from tg_devices.weight.weights import VersionWeights

WINDOWS_PLATFORM_DEFAULTS: Final[dict[str, WeightCurveParams]] = (
    PLATFORM_DEFAULTS[OS.WINDOWS]
)

WINDOWS_APP_WEIGHT_MAP: Final[Mapping[WindowsAppVersion, int]] = (
    compute_weights(WindowsAppVersion, params=WINDOWS_PLATFORM_DEFAULTS["app"])
)

WINDOWS_SYSTEM_WEIGHT_MAP: Final[Mapping[WindowsSystemVersion, int]] = (
    compute_weights(
        WindowsSystemVersion, params=WINDOWS_PLATFORM_DEFAULTS["sys"]
    )
)

WINDOWS_APP_VERSIONS: Final = tuple(WINDOWS_APP_WEIGHT_MAP.keys())
WINDOWS_APP_WEIGHTS: Final = tuple(WINDOWS_APP_WEIGHT_MAP.values())

WINDOWS_SYSTEM_VERSIONS: Final = tuple(WINDOWS_SYSTEM_WEIGHT_MAP.keys())
WINDOWS_SYSTEM_WEIGHTS: Final = tuple(WINDOWS_SYSTEM_WEIGHT_MAP.values())

WINDOWS_COMPATIBILITY_MAP: Final[
    dict[SystemVersion, tuple[tuple[AppVersion, ...], tuple[int, ...]]]
] = get_compatibility_map(
    OS.WINDOWS,
    WINDOWS_APP_VERSIONS,
    WINDOWS_APP_WEIGHTS,
    WINDOWS_SYSTEM_VERSIONS,
)

WINDOWS_DEVICE_MODELS: Final[tuple[WindowsDesktopModel, ...]] = tuple(
    WindowsDesktopModel
)

WINDOWS_WEIGHTS_DATA: Final[VersionWeights] = VersionWeights(
    WINDOWS_APP_WEIGHTS, WINDOWS_SYSTEM_WEIGHTS
)
