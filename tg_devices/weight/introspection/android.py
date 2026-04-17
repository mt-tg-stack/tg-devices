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
from tg_devices.weight.weights import VersionWeights

ANDROID_APP_WEIGHTS: Final[Mapping[AndroidAppVersion, int]] = {
    AndroidAppVersion.V8_9_3: 1,
    AndroidAppVersion.V9_6_5: 1,
    AndroidAppVersion.V10_0_1: 2,
    AndroidAppVersion.V10_1_0: 2,
    AndroidAppVersion.V10_2_3: 3,
    AndroidAppVersion.V10_3_2: 3,
    AndroidAppVersion.V10_4_1: 4,
    AndroidAppVersion.V10_5_0: 5,
    AndroidAppVersion.V10_6_1: 5,
    AndroidAppVersion.V10_7_0: 6,
    AndroidAppVersion.V10_8_1: 8,
    AndroidAppVersion.V10_9_0: 8,
    AndroidAppVersion.V10_10_1: 10,
    AndroidAppVersion.V10_11_0: 12,
    AndroidAppVersion.V10_12_0: 15,
    AndroidAppVersion.V10_13_0: 20,
    AndroidAppVersion.V10_14_0: 25,
    AndroidAppVersion.V11_0_0: 30,
    AndroidAppVersion.V11_1_2: 30,
    AndroidAppVersion.V11_2_0: 30,
    AndroidAppVersion.V11_3_4: 25,
    AndroidAppVersion.V11_4_1: 25,
    AndroidAppVersion.V11_5_0: 20,
    AndroidAppVersion.V11_6_2: 20,
    AndroidAppVersion.V11_7_1: 15,
    AndroidAppVersion.V11_8_0: 15,
    AndroidAppVersion.V11_9_3: 10,
    AndroidAppVersion.V12_0_0: 10,
    AndroidAppVersion.V12_1_1: 8,
    AndroidAppVersion.V12_2_3: 8,
    AndroidAppVersion.V12_3_0: 6,
    AndroidAppVersion.V12_4_2: 5,
    AndroidAppVersion.V12_5_0: 5,
}

ANDROID_SYSTEM_WEIGHTS: Final[Mapping[AndroidSystemVersion, int]] = {
    AndroidSystemVersion.ANDROID_6_0: 1,
    AndroidSystemVersion.ANDROID_7_0: 1,
    AndroidSystemVersion.ANDROID_7_1: 1,
    AndroidSystemVersion.ANDROID_8_0: 2,
    AndroidSystemVersion.ANDROID_8_1: 2,
    AndroidSystemVersion.ANDROID_9_0: 3,
    AndroidSystemVersion.ANDROID_10_0: 4,
    AndroidSystemVersion.ANDROID_11_0: 6,
    AndroidSystemVersion.ANDROID_12_0: 8,
    AndroidSystemVersion.ANDROID_12_1: 2,
    AndroidSystemVersion.ANDROID_13_0: 15,
    AndroidSystemVersion.ANDROID_14_0: 25,
    AndroidSystemVersion.ANDROID_15_0: 20,
    AndroidSystemVersion.ANDROID_16_0: 8,
    AndroidSystemVersion.ANDROID_17_0: 2,
}

ANDROID_APPS: Final = tuple(ANDROID_APP_WEIGHTS.keys())
ANDROID_APPS_WEIGHTS: Final = tuple(ANDROID_APP_WEIGHTS.values())

ANDROID_SYSTEMS: Final = tuple(ANDROID_SYSTEM_WEIGHTS.keys())
ANDROID_SYSTEMS_WEIGHTS: Final = tuple(ANDROID_SYSTEM_WEIGHTS.values())

ANDROID_COMPATIBILITY_MAP: Final[
    dict[SystemVersion, tuple[tuple[AppVersion, ...], tuple[int, ...]]]
] = get_compatibility_map(
    OS.ANDROID, ANDROID_APPS, ANDROID_APPS_WEIGHTS, ANDROID_SYSTEMS
)

ANDROID_DEVICE_MODEL: Final[tuple[AndroidModel, ...]] = tuple(AndroidModel)

ANDROID_WEIGHTS_DT: Final[VersionWeights] = VersionWeights(
    ANDROID_APPS_WEIGHTS, ANDROID_SYSTEMS_WEIGHTS
)
