"""Pre-computed static weight data for Linux."""

from collections.abc import Mapping
from typing import Final

from tg_devices.compatibility.map import get_compatibility_map
from tg_devices.enums.app_version import AppVersion
from tg_devices.enums.linux import (
    LinuxAppVersion,
    LinuxDesktopModel,
    LinuxSystemVersion,
)
from tg_devices.enums.os import OS
from tg_devices.enums.system_version import SystemVersion
from tg_devices.weight.introspection.weight_precomputation import (
    PLATFORM_DEFAULTS,
    compute_weights,
)
from tg_devices.weight.weights import VersionWeights

LINUX_APP_WEIGHT_MAP: Final[Mapping[LinuxAppVersion, int]] = compute_weights(
    LinuxAppVersion, params=PLATFORM_DEFAULTS["linux_app"]
)

LINUX_SYSTEM_WEIGHT_MAP: Final[Mapping[LinuxSystemVersion, int]] = (
    compute_weights(LinuxSystemVersion, params=PLATFORM_DEFAULTS["linux_sys"])
)

LINUX_APP_VERSIONS: Final = tuple(LINUX_APP_WEIGHT_MAP.keys())
LINUX_APP_WEIGHTS: Final = tuple(LINUX_APP_WEIGHT_MAP.values())

LINUX_SYSTEM_VERSIONS: Final = tuple(LINUX_SYSTEM_WEIGHT_MAP.keys())
LINUX_SYSTEM_WEIGHTS: Final = tuple(LINUX_SYSTEM_WEIGHT_MAP.values())

LINUX_COMPATIBILITY_MAP: Final[
    dict[SystemVersion, tuple[tuple[AppVersion, ...], tuple[int, ...]]]
] = get_compatibility_map(
    OS.LINUX, LINUX_APP_VERSIONS, LINUX_APP_WEIGHTS, LINUX_SYSTEM_VERSIONS
)

LINUX_DEVICE_MODELS: Final[tuple[LinuxDesktopModel, ...]] = tuple(
    LinuxDesktopModel
)

LINUX_WEIGHTS_DATA: Final[VersionWeights] = VersionWeights(
    LINUX_APP_WEIGHTS, LINUX_SYSTEM_WEIGHTS
)
