"""Pre-computed static weight data for macOS."""

from collections.abc import Mapping
from typing import Final

from tg_devices.compatibility.map import get_compatibility_map
from tg_devices.enums.app_version import AppVersion
from tg_devices.enums.macos import (
    MacOSAppVersion,
    MacOSDesktopModel,
    MacOSSystemVersion,
)
from tg_devices.enums.os import OS
from tg_devices.enums.system_version import SystemVersion
from tg_devices.weight.introspection.weight_precomputation import (
    PLATFORM_DEFAULTS,
    compute_weights,
)
from tg_devices.weight.weights import VersionWeights

MACOS_APP_WEIGHT_MAP: Final[Mapping[MacOSAppVersion, int]] = compute_weights(
    MacOSAppVersion, params=PLATFORM_DEFAULTS["macos_app"]
)

MACOS_SYSTEM_WEIGHT_MAP: Final[Mapping[MacOSSystemVersion, int]] = (
    compute_weights(MacOSSystemVersion, params=PLATFORM_DEFAULTS["macos_sys"])
)

MACOS_APP_VERSIONS: Final = tuple(MACOS_APP_WEIGHT_MAP.keys())
MACOS_APP_WEIGHTS: Final = tuple(MACOS_APP_WEIGHT_MAP.values())

MACOS_SYSTEM_VERSIONS: Final = tuple(MACOS_SYSTEM_WEIGHT_MAP.keys())
MACOS_SYSTEM_WEIGHTS: Final = tuple(MACOS_SYSTEM_WEIGHT_MAP.values())

MACOS_COMPATIBILITY_MAP: Final[
    dict[SystemVersion, tuple[tuple[AppVersion, ...], tuple[int, ...]]]
] = get_compatibility_map(
    OS.MACOS, MACOS_APP_VERSIONS, MACOS_APP_WEIGHTS, MACOS_SYSTEM_VERSIONS
)

MACOS_DEVICE_MODELS: Final[tuple[MacOSDesktopModel, ...]] = tuple(
    MacOSDesktopModel
)

MACOS_WEIGHTS_DATA: Final[VersionWeights] = VersionWeights(
    MACOS_APP_WEIGHTS, MACOS_SYSTEM_WEIGHTS
)
