"""Pre-computed static weight data for Windows."""

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
    compute_weights,
)
from tg_devices.weight.weights import VersionWeights

WINDOWS_APP_WEIGHT_MAP: Final[Mapping[WindowsAppVersion, int]] = (
    compute_weights(WindowsAppVersion, params=PLATFORM_DEFAULTS["windows_app"])
)

WINDOWS_SYSTEM_WEIGHT_MAP: Final[Mapping[WindowsSystemVersion, int]] = (
    compute_weights(
        WindowsSystemVersion, params=PLATFORM_DEFAULTS["windows_sys"]
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
