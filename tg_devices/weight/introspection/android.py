"""Pre-computed static weight data for Android."""

from collections.abc import Mapping
from typing import Final

from tg_devices.compatibility.map import get_compatibility_map
from tg_devices.enums.android import (
    AndroidAppVersion,
    AndroidModel,
    AndroidSystemVersion,
)
from tg_devices.enums.app_version import AppVersion
from tg_devices.enums.os import OS
from tg_devices.enums.system_version import SystemVersion
from tg_devices.weight.introspection.weight_precomputation import (
    PLATFORM_DEFAULTS,
    compute_weights,
)
from tg_devices.weight.weights import VersionWeights

ANDROID_APP_WEIGHT_MAP: Final[Mapping[AndroidAppVersion, int]] = (
    compute_weights(AndroidAppVersion, params=PLATFORM_DEFAULTS["android_app"])
)

ANDROID_SYSTEM_WEIGHT_MAP: Final[Mapping[AndroidSystemVersion, int]] = (
    compute_weights(
        AndroidSystemVersion, params=PLATFORM_DEFAULTS["android_sys"]
    )
)


ANDROID_APP_VERSIONS: Final = tuple(ANDROID_APP_WEIGHT_MAP.keys())
ANDROID_APP_WEIGHTS: Final = tuple(ANDROID_APP_WEIGHT_MAP.values())

ANDROID_SYSTEM_VERSIONS: Final = tuple(ANDROID_SYSTEM_WEIGHT_MAP.keys())
ANDROID_SYSTEM_WEIGHTS: Final = tuple(ANDROID_SYSTEM_WEIGHT_MAP.values())

ANDROID_COMPATIBILITY_MAP: Final[
    dict[SystemVersion, tuple[tuple[AppVersion, ...], tuple[int, ...]]]
] = get_compatibility_map(
    OS.ANDROID,
    ANDROID_APP_VERSIONS,
    ANDROID_APP_WEIGHTS,
    ANDROID_SYSTEM_VERSIONS,
)

ANDROID_DEVICE_MODELS: Final[tuple[AndroidModel, ...]] = tuple(AndroidModel)

ANDROID_WEIGHTS_DATA: Final[VersionWeights] = VersionWeights(
    ANDROID_APP_WEIGHTS, ANDROID_SYSTEM_WEIGHTS
)
